import os
import requests

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def query_hf_api(model_name, payload):
    """Generic function to query Hugging Face API"""
    API_URL = f"https://router.huggingface.co/models/{model_name}"
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

def extract_keywords(text):
    """
    Extract keywords using Keyphrase Extraction
    Model: ml6team/keyphrase-extraction-kbir-inspec
    """
    try:
        result = query_hf_api(
            "ml6team/keyphrase-extraction-kbir-inspec",
            {"inputs": text}
        )
        
        if isinstance(result, list):
            keywords = set()
            for item in result:
                if isinstance(item, dict) and "word" in item:
                    keyword = item["word"].strip()
                    keyword = keyword.replace("##", "")
                    if keyword:
                        keywords.add(keyword)
            return list(keywords)
        
        if isinstance(result, dict) and "error" in result:
            print(f"API Error: {result['error']}")
            return []
        
        return []
    except Exception as e:
        print(f"Error in extract_keywords: {str(e)}")
        return []