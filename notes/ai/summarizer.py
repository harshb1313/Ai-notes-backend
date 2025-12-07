import os
import requests

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def query_hf_api(model_name, payload):
    """Generic function to query Hugging Face API"""
    API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

def summarize_text(text):
    """
    Summarize text using BART Large CNN
    Model: facebook/bart-large-cnn
    """
    try:
        result = query_hf_api(
            "facebook/bart-large-cnn",
            {
                "inputs": text,
                "parameters": {
                    "max_length": 180,
                    "min_length": 30,
                    "do_sample": False
                }
            }
        )
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("summary_text", "")
        if isinstance(result, dict):
            if "error" in result:
                print(f"API Error: {result['error']}")
                return "Summarization unavailable"
            return result.get("summary_text", "")
        return "Summary unavailable"
    except Exception as e:
        print(f"Error in summarize_text: {str(e)}")
        return "Summary unavailable"
