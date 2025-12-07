import os
import requests
import time

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def query_hf_api(model_name, payload, max_retries=3):
    """
    Generic function to query Hugging Face API with retry logic
    """
    API_URL = f"https://router.huggingface.co/models/{model_name}"
    
    for attempt in range(max_retries):
        try:
            print(f"[Attempt {attempt + 1}/{max_retries}] Calling {model_name}")
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
            result = response.json()
            
            # Log the raw response for debugging
            print(f"Response status: {response.status_code}")
            print(f"Response body: {result}")
            
            # Check if model is loading
            if isinstance(result, dict) and "error" in result:
                error_msg = result["error"]
                
                # Model is loading - wait and retry
                if "loading" in error_msg.lower() or "is currently loading" in error_msg.lower():
                    wait_time = result.get("estimated_time", 20)
                    print(f"Model loading... waiting {wait_time}s")
                    time.sleep(wait_time + 5)  # Add 5s buffer
                    continue
                
                # Rate limit or other errors
                print(f"API Error: {error_msg}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                return None
            
            # Check response status
            if response.status_code != 200:
                print(f"HTTP Error {response.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                return None
            
            # Success
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

def summarize_text(text):
    """
    Summarize text using BART Large CNN
    Model: facebook/bart-large-cnn
    """
    try:
        print(f"Starting summarization for text of length: {len(text)}")
        
        # Truncate if too long (BART has max input length)
        max_length = 1024
        if len(text) > max_length:
            text = text[:max_length]
            print(f"Text truncated to {max_length} characters")
        
        result = query_hf_api(
            "facebook/bart-large-cnn",
            {
                "inputs": text,
                "parameters": {
                    "max_length": 150,
                    "min_length": 30,
                    "do_sample": False
                }
            }
        )
        
        if not result:
            print("No result from API")
            return "Summarization unavailable"
        
        if isinstance(result, list) and len(result) > 0:
            summary = result[0].get("summary_text", "")
            if summary:
                print(f"Summary generated: {summary[:50]}...")
                return summary
        
        if isinstance(result, dict):
            summary = result.get("summary_text", "")
            if summary:
                print(f"Summary generated: {summary[:50]}...")
                return summary
        
        print("Could not extract summary from response")
        return "Summary unavailable"
        
    except Exception as e:
        print(f"Error in summarize_text: {str(e)}")
        return "Summary unavailable"