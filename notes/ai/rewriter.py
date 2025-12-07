import os
import requests

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def query_hf_api(model_name, payload):
    """Generic function to query Hugging Face API"""
    API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

def paraphrase_text(text):
    """
    Paraphrase text using T5 Paraphraser
    Model: ramsrigouthamg/t5_paraphraser
    """
    try:
        input_text = f"paraphrase: {text} </s>"
        result = query_hf_api(
            "ramsrigouthamg/t5_paraphraser",
            {
                "inputs": input_text,
                "parameters": {
                    "max_length": 256,
                    "top_k": 120,
                    "top_p": 0.98,
                    "do_sample": True
                }
            }
        )
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "")
        if isinstance(result, dict):
            if "error" in result:
                print(f"API Error: {result['error']}")
                return "Paraphrasing unavailable"
            return result.get("generated_text", "")
        return text
    except Exception as e:
        print(f"Error in paraphrase_text: {str(e)}")
        return text