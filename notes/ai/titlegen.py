import os
import requests
import time

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def query_hf_api(model_name, payload, max_retries=3):
    """
    Generic function to query Hugging Face API with retry logic
    """
    API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
    
    for attempt in range(max_retries):
        try:
            print(f"[Attempt {attempt + 1}/{max_retries}] Calling {model_name}")
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
            result = response.json()
            
            print(f"Response status: {response.status_code}")
            print(f"Response body: {result}")
            
            if isinstance(result, dict) and "error" in result:
                error_msg = result["error"]
                
                if "loading" in error_msg.lower() or "is currently loading" in error_msg.lower():
                    wait_time = result.get("estimated_time", 20)
                    print(f"Model loading... waiting {wait_time}s")
                    time.sleep(wait_time + 5)
                    continue
                
                print(f"API Error: {error_msg}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                return None
            
            if response.status_code != 200:
                print(f"HTTP Error {response.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                return None
            
            return result
            
        except requests.exceptions.Timeout:
            print(f"Request timeout")
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
        except Exception as e:
            print(f"Exception: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
    
    return None

def createTitle(text):
    """
    Generate title using Flan-T5 Base
    Model: google/flan-t5-base
    """
    try:
        print(f"Starting title generation for text of length: {len(text)}")
        
        text_snippet = text[:200] if len(text) > 200 else text
        
        prompt = f"generate title: {text_snippet}"
        result = query_hf_api(
            "google/flan-t5-base",
            {
                "inputs": prompt,
                "parameters": {
                    "max_length": 64,
                    "top_k": 60,
                    "top_p": 0.9,
                    "do_sample": True
                }
            }
        )
        
        if not result:
            print("No result from API")
            return "Untitled"
        
        if isinstance(result, list) and len(result) > 0:
            title = result[0].get("generated_text", "")
            if title:
                print(f"Generated title: {title}")
                return title
        
        if isinstance(result, dict):
            title = result.get("generated_text", "")
            if title:
                print(f"Generated title: {title}")
                return title
        
        return "Untitled"
        
    except Exception as e:
        print(f"Error in createTitle: {str(e)}")
        return "Untitled"