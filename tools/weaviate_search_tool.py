import json
from typing import Type
import nest_asyncio
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

# Import project-specific modules
from config.weaviate_setup.weaviate_cloud_conn import create_connection_with_weaviate_cloud
from tools.weaviate_tools.vectorizer import model

# Apply asyncio patch if running in an environment like Jupyter/Colab
nest_asyncio.apply()




class WeaviateToolSchema(BaseModel):
    """Input schema for the WeaviateTool."""
    query: str = Field(..., description="The user's original search query for vector search.")
    intent: str = Field(..., description="The classified intent (e.g., 'activity', 'dish') which maps to a Weaviate collection.")


class WeaviateTool(BaseTool):
    name: str = "Weaviate Vector Search"
    description: str = "Performs a vector search in the Weaviate database based on a query and a specific data intent (e.g., 'activity', 'restaurant')."
    args_schema: Type[BaseModel] = WeaviateToolSchema

    def _run(self, query: str, intent: str) -> str:
        """
        Executes the Weaviate search.
        
        This method connects to Weaviate, maps the intent to the correct collection
        and properties, performs a near_vector search, and returns the results
        as a JSON string with a key that matches the expected Pydantic schema.
        """
        print(f"\n[WeaviateTool] Initializing for intent: '{intent}' with query: '{query}'")
        client = None
        try:
            client = create_connection_with_weaviate_cloud()
            if not client:
                return json.dumps({"error": "Failed to establish a connection with Weaviate."})

            # Maps intent to Weaviate collection name and the properties to retrieve
            collection_map = {
                "activity": {"name": "Activity", "properties": ["Country", "City", "Activity", "Description", "TypeOfTraveler", "Duration", "BudgetInUSD", "BudgetDetails", "TipsAndRecommendations", "For", "FamilyFriendly", "Category"]},
                "dish": {"name": "Dishes", "properties": ["Country", "City", "DishName", "DishDetails", "Type", "AvgPriceInUSD", "BestFor"]},
                "restaurant": {"name": "Restaurants", "properties": ["Country", "City", "RestaurantName", "TypeOfCuisine", "MealsServed", "RecommendedDish", "MealDescription", "AvgPricePerPersonInUSD", "BudgetRange", "Suitability"]},
                "scam": {"name": "Scams", "properties": ["Country", "City", "ScamType", "Description", "Location", "PreventionTips"]},
                "accommodation": {"name": "Accommodations", "properties": ["Country", "City", "AccommodationName", "AccommodationDetails", "Type", "AvgNightPriceInUSD"]},
                "transportation": {"name": "Transportation", "properties": ["Country", "From", "To", "TransportMode", "Provider", "Schedule", "RouteInfo", "DurationInHours", "PriceRangeInUSD", "CostDetailsAndOptions", "AdditionalInfo"]},
                "visa": {"name": "Visa", "properties": ["Country", "Question", "Answer"]},
                "seasonal": {"name": "Seasonal", "properties": ["Country", "Question", "Answer"]}
            }
            
            # Maps intent to the JSON output key expected by the Pydantic schemas in the crew
            output_key_map = {
                "activity": "activities", "dish": "dishes", "restaurant": "restaurants",
                "scam": "scams", "accommodation": "accommodations", "transportation": "transportations",
                "visa": "visas", "seasonal": "seasonals"
            }

            intent_clean = intent.lower().strip()
            if intent_clean not in collection_map:
                return json.dumps({"error": f"Unknown intent '{intent_clean}'. No matching collection configured."})

            collection_config = collection_map[intent_clean]
            collection_name = collection_config["name"]
            return_properties = collection_config["properties"]
            output_key = output_key_map[intent_clean]

            print(f"[WeaviateTool] Searching in collection: '{collection_name}'")
            collection = client.collections.get(collection_name)
            
            # Generate vector for the query
            query_vector = model.encode(query).tolist()
            
            # Perform the near-vector search
            response = collection.query.near_vector(
                near_vector=query_vector,
                limit=15,
                certainty=0.65,
                return_properties=return_properties
            )
            
            # Extract properties from the response objects
            rag_results = [obj.properties for obj in response.objects]
            print(f"[WeaviateTool] Found {len(rag_results)} results for intent '{intent_clean}'.")
            
            # Structure the output to match the Pydantic schema key
            output_dict = {output_key: rag_results}
            
            return json.dumps(output_dict)

        except Exception as e:
            print(f"[WeaviateTool] An error occurred: {e}")
            return json.dumps({"error": str(e)})
        finally:
            if client:
                client.close()
                print(f"[WeaviateTool] Connection to Weaviate closed.")