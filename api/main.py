import sys
import os
import nest_asyncio
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pyngrok import ngrok
import uvicorn

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from core.agents.rag_crew import AgenticRagCrew

nest_asyncio.apply()

app = FastAPI(title="Agentic RAG Crew API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Initializing Agentic RAG Crew...")
crew = AgenticRagCrew()
print("Crew initialized successfully.")

UI_DIR = os.path.join(PROJECT_ROOT, "ui")
INDEX_HTML_PATH = os.path.join(UI_DIR, "index.html")

@app.get("/", response_class=FileResponse)
def serve_html():
    if not os.path.exists(INDEX_HTML_PATH):
        return {"error": "index.html not found"}
    return FileResponse(INDEX_HTML_PATH)

@app.get("/api/run_crew")
def run_crew(query: str = Query(..., description="The user's query for the agent crew.")):
    try:
        print(f"Received API request with query: {query}")
        result = crew.run_task_by_classified_intent(query)
        return result
    except Exception as e:
        print(f"Error during crew execution: {e}")
        return {"error": f"An error occurred: {str(e)}"}

if __name__ == "__main__":
    print("Starting server and creating ngrok tunnel...")
    
    public_url = ngrok.connect(8000).public_url
    print(f"FastAPI server is running at {public_url}")

    try:
        with open(INDEX_HTML_PATH, "r") as f:
            html_content = f.read()
        updated_html = html_content.replace("YOUR_API_ENDPOINT_PLACEHOLDER", public_url)
        with open(INDEX_HTML_PATH, "w") as f:
            f.write(updated_html)
        print(f"UI updated at {INDEX_HTML_PATH}")
    except FileNotFoundError:
        print(f"UI file not found at {INDEX_HTML_PATH}")

    uvicorn.run(app, host="0.0.0.0", port=8000)