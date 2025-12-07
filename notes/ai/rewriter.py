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

def paraphrase_text(text):
    """
    Paraphrase text using T5 Paraphraser
    Model: ramsrigouthamg/t5_paraphraser
    """
    try:
        print(f"Starting paraphrasing for text of length: {len(text)}")
        
        max_length = 512
        if len(text) > max_length:
            text = text[:max_length]
        
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
        
        if not result:
            print("No result from API")
            return text
        
        if isinstance(result, list) and len(result) > 0:
            paraphrased = result[0].get("generated_text", "")
            if paraphrased:
                return paraphrased
        
        if isinstance(result, dict):
            paraphrased = result.get("generated_text", "")
            if paraphrased:
                return paraphrased
        
        return text
        
    except Exception as e:
        print(f"Error in paraphrase_text: {str(e)}")
        return text