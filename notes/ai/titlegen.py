import os
import requests

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def query_hf_api(model_name, payload):
    """Generic function to query Hugging Face API"""
    API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

def createTitle(text):
    """
    Generate title using Flan-T5 Base
    Model: google/flan-t5-base
    """
    try:
        prompt = f"generate title: {text}"
        result = query_hf_api(
            "google/flan-t5-base",
            {
                "inputs": prompt,
                "parameters": {
                    "max_length": 128,
                    "top_k": 60,
                    "top_p": 0.9,
                    "do_sample": True
                }
            }
        )
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "")
        if isinstance(result, dict):
            if "error" in result:
                print(f"API Error: {result['error']}")
                return "Title generation unavailable"
            return result.get("generated_text", "")
        return "Untitled"
    except Exception as e:
        print(f"Error in createTitle: {str(e)}")
        return "Untitled"