🤖 Agentic RAG Travel Assistant

This project implements a sophisticated multi-agent system designed to act as an intelligent travel assistant. It uses a combination of Retrieval-Augmented Generation (RAG), local and cloud-based Large Language Models (LLMs), and specialized agents to provide detailed and context-aware answers to a wide range of travel-related queries.

The system can dynamically classify a user's intent (e.g., asking about accommodations, restaurants, or local scams) and delegate the task to the appropriate specialized agent. Each agent then retrieves relevant information from a Weaviate vector database and uses an LLM to generate a structured, helpful response.

✨ Key Features

Multi-Agent System: Built with CrewAI, orchestrating multiple specialized agents for different tasks.

Dynamic Intent Classification: Automatically determines the user's goal (e.g., finding activities, restaurants, visa info) to activate the correct agent.

Retrieval-Augmented Generation (RAG): Agents retrieve up-to-date, relevant information from a Weaviate vector database, preventing hallucinations and providing factual data.

Hybrid LLM Approach: Utilizes Ollama for local agent processing (e.g., llama3.1) and the Google Gemini API for high-speed tasks like filtering and classification.

API-First Design: A robust FastAPI backend serves the agentic logic, making it easy to integrate with any frontend.

Live Web Interface: Comes with a simple, interactive UI served via Ngrok for easy demonstration and testing.

Structured Outputs: Uses Pydantic models to ensure agents return clean, predictable JSON data.

🏗️ System Architecture

The project follows a modular, RAG-based architecture where user queries are processed through a pipeline of classification, retrieval, and generation.

Generated mermaid
graph TD
    A[User via Browser UI] -->|HTTP Request| B(FastAPI Backend);
    B --> C{AgenticRagCrew};
    C -->|1. Classify Intent| D[Intent Classifier Service];
    D -->|e.g., "restaurant"| C;
    C -->|2. Select Agent| E[Restaurant Agent];
    E -->|3. Use Tool| F(Weaviate Search Tool);
    F -->|4. Vector Search Query| G[(Weaviate Vector DB)];
    G -->|5. Return Relevant Docs| F;
    F -->|6. Return JSON Data| E;
    E -->|7. Generate Final Answer with LLM| H(Ollama / Llama 3.1);
    H -->|8. Structured JSON Output| C;
    C -->|9. Final API Response| B;
    B -->|HTTP Response| A;

🛠️ Tech Stack

AI Framework: CrewAI & LangChain

Backend: FastAPI

Local LLM Server: Ollama

Cloud LLM API: Google Gemini

Vector Database: Weaviate

Vector Embeddings: Sentence-Transformers

Web Server: Uvicorn

Tunneling: Ngrok

Data Validation: Pydantic

📂 Project Structure
Generated code
/Agentic_Rag/
├── api/
│   └── main.py              # FastAPI application entry point
├── core/
│   ├── agents/
│   │   └── rag_crew.py      # Core CrewAI logic, agent/task definitions
│   ├── models/
│   │   └── schemas.py       # Pydantic schemas for structured output
│   └── services/
│       └── classification.py# Intent classification logic
├── tools/
│   ├── weaviate_search_tool.py # Custom CrewAI tool for Weaviate
│   └── weaviate_tools/
│       └── vectorizer.py    # Sentence-Transformer model loader
├── ui/
│   └── index.html           # Simple frontend for interaction
├── config/
│   └── weaviate_setup/      # Weaviate connection and schema setup
├── tests/
│   └── test.py              # Unit and integration tests
├── .env.example             # Example environment variables file
├── requirements.txt         # Python package dependencies
└── README.md                # You are here
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
🚀 Getting Started

Follow these steps to set up and run the project locally.

1. Prerequisites

Python 3.10+

Docker and Docker Compose (for running Weaviate)

An account with Ngrok to get an authentication token.

A Google AI Studio account to get a Gemini API key.

2. Installation

Clone the repository:

Generated bash
git clone https://github.com/Anasmahmoud00/Agentic_Rag.git
cd Agentic_Rag
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Create a virtual environment and activate it:

Generated bash
python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Install the required Python packages:

Generated bash
pip install -r requirements.txt
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
3. Local Services Setup

Start Ollama Server:
You need a running Ollama instance. Download it from ollama.ai and run the server. Then, pull the required model:

Generated bash
ollama pull llama3.1:8b-instruct-q8_0
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Start Weaviate Database:
The project includes a docker-compose.yml for Weaviate. Run it from the root directory:

Generated bash
docker-compose up -d
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Note: You will also need to run the scripts in /tools/weaviate_tools/insert_data/ to populate the database with your travel data.

4. Configuration

Create a .env file in the root directory by copying the example:

Generated bash
cp .env.example .env
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Edit the .env file and add your secret keys:

Generated env
# Get from Google AI Studio
GEMINI_API_KEY="AIzaSy..."

# Get from your ngrok dashboard
NGROK_AUTH_TOKEN="2yrm7j..."

# Weaviate connection details (matches docker-compose.yml)
WEAVIATE_URL="http://localhost:8080"
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Env
IGNORE_WHEN_COPYING_END
5. Running the Application

Once all services are running and your .env file is configured, start the main application:

Generated bash
python api/main.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

The terminal will display the public ngrok URL.

Generated code
🚀 FastAPI server is running.
🔗 PUBLIC URL: https://<some-random-string>.ngrok-free.app
✅ UI file updated. Open the UI at: https://<some-random-string>.ngrok-free.app
...
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END

Open the provided URL in your browser to interact with the travel assistant.

🤖 API Usage

You can also interact with the API directly using curl or any API client.

Endpoint: GET /api/run_crew

Example Request:

Generated bash
curl -X GET "https://<your-ngrok-url>.ngrok-free.app/api/run_crew?query=what+are+some+good+activities+in+tokyo"
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
📈 Future Improvements

Implement more specialized agents (e.g., for flight booking, cultural etiquette).

Enhance the RAG filtering and ranking logic for more precise results.

Develop a more feature-rich frontend using a framework like React or Vue.

Add comprehensive unit and integration tests for all components.

Implement caching for frequently asked questions to improve performance.
