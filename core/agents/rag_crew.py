import os
import json
from typing import Dict, Any
import google.generativeai as genai
from crewai import Agent, Crew, Process, Task
from core.models.schemas import (
    ActivityOutputSchema, AccommodationOutputSchema, DishOutputSchema,
    RestaurantOutputSchema, ScamOutputSchema, SeasonalOutputSchema,
    TransportationOutputSchema, VisaOutputSchema
)
from core.services.classification import classify_query_intent
from tools.weaviate_search_tool import WeaviateTool

class AgenticRagCrew:
    def __init__(self):
        # Configure Gemini
        gemini_api_key = "AIzaSyAwFg8n9A1Wq2FGzMY-J6Ux7fYBAPj1lEs"
        genai.configure(api_key=gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Create output directory
        os.makedirs("outputs", exist_ok=True)
        
        self._create_agents_and_tasks()

    def _create_agents_and_tasks(self):
        agent_configs = {
            "activity": {"role": "Activity Specialist", "goal": "Find travel activities", "output_schema": ActivityOutputSchema},
            "accommodation": {"role": "Accommodation Specialist", "goal": "Find places to stay", "output_schema": AccommodationOutputSchema},
            "dish": {"role": "Local Cuisine Expert", "goal": "Find local dishes", "output_schema": DishOutputSchema},
            "restaurant": {"role": "Restaurant Expert", "goal": "Find places to eat", "output_schema": RestaurantOutputSchema},
            "scam": {"role": "Safety Advisor", "goal": "Find information on common scams", "output_schema": ScamOutputSchema},
            "seasonal": {"role": "Seasonal Travel Advisor", "goal": "Find the best time to travel", "output_schema": SeasonalOutputSchema},
            "transportation": {"role": "Transportation Specialist", "goal": "Find how to get around", "output_schema": TransportationOutputSchema},
            "visa": {"role": "Visa & Entry Advisor", "goal": "Find visa requirements", "output_schema": VisaOutputSchema},
        }

        self.agents = {}
        self.tasks = {}

        for intent, config in agent_configs.items():
            self.agents[intent] = Agent(
                role=config["role"],
                goal=f"{config['goal']} based on user queries from a Weaviate database.",
                backstory=f"You are an expert in retrieving information about {intent}.",
                tools=[WeaviateTool()],
                verbose=True
            )
            
            self.tasks[intent] = Task(
                description=f"Find relevant information about '{intent}' for query: '{{query}}'",
                expected_output=f"JSON data about {intent}",
                output_json=config["output_schema"],
                output_file=os.path.join("outputs", f"{intent}_result.json"),
                agent=self.agents[intent]
            )

    def run_task_by_classified_intent(self, query: str) -> Dict[str, Any]:
        intent_result = classify_query_intent(query)
        
        if intent_result == "unknown":
            return {"error": "Could not determine query intent"}
            
        intents = [intent_result] if isinstance(intent_result, str) else intent_result
        
        final_results = {}
        for intent in intents:
            if intent not in self.tasks:
                continue
                
            crew = Crew(
                agents=[self.agents[intent]],
                tasks=[self.tasks[intent]],
                process=Process.sequential,
                verbose=1
            )
            final_results[self.agents[intent].role] = crew.kickoff(inputs={'query': query})

        if not final_results:
            return {"error": "No results generated"}
            
        with open("outputs/final_crew_results.json", "w") as f:
            json.dump(final_results, f, indent=4)

        return final_results