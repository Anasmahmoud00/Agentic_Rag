# /content/Basir_RAG_Agents/core/services/classification.py

import requests
import re

# Define your Ollama model ID consistently
OLLAMA_MODEL_ID = "llama3.1:8b-instruct-q8_0"
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def classify_query_intent(query: str):
    """
    Classifies the user's query into one or more predefined categories
    by prompting a local LLM.
    """
    # Clean the input query
    query = query.strip().replace("\n", " ").replace("\r", " ")

    # The prompt instructs the LLM on how to behave
    system_prompt = (
        "You are a classification expert. Classify the user's query into one or more of the following categories "
        "depending on relevance:\n"
        "- activity\n"
        "- accommodation\n"
        "- visa\n"
        "- scam\n"
        "- dish\n"
        "- transportation\n"
        "- seasonal\n"
        "- restaurant\n\n"
        "Rules:\n"
        "- Reply with a comma-separated list of relevant categories (e.g., visa, restaurant).\n"
        "- Do NOT explain. Do NOT add anything else. ONLY output the category names.\n"
        "- If only one category applies, return just that one word.\n"
        "- Only use the category names listed above. No synonyms or other text.\n\n"
        f"Query: {query}\nLabels:"
    )

    payload = {
        "model": OLLAMA_MODEL_ID,
        "prompt": system_prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()  # This will raise an exception for HTTP errors (4xx or 5xx)

        # Extract, clean, and validate the labels from the LLM response
        raw_text = response.json()["response"].strip().lower()
        valid_labels = ["activity", "accommodation", "visa", "restaurant", "scam", "transportation", "dish", "seasonal"]
        
        # Find all valid labels in the response string
        found_labels = [label for label in re.split(r'[,\s]+', raw_text) if label in valid_labels]

        if not found_labels:
            return "unknown"
        elif len(found_labels) == 1:
            return found_labels[0]
        else:
            return found_labels

    except requests.exceptions.RequestException as e:
        print(f"[Intent Classifier Error] Network or API error: {e}")
        return "unknown"
    except Exception as e:
        print(f"[Intent Classifier Error] An unexpected error occurred: {e}")
        return "unknown"