import os
from huggingface_hub import InferenceClient

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def extract_keywords(text):
    """
    Extract keywords using a chat model
    Using meta-llama model which is reliable and fast
    """
    try:
        print(f"Starting keyword extraction for text of length: {len(text)}")
        
        # Truncate if too long
        max_length = 512
        if len(text) > max_length:
            text = text[:max_length]
        
        # Create InferenceClient with the NEW base URL
        client = InferenceClient(
            token=HUGGINGFACE_API_KEY,
            base_url="https://router.huggingface.co"
        )
        
        # Use chat completion with a prompt to extract keywords
        messages = [
            {
                "role": "user",
                "content": f"Extract 5-10 important keywords or key phrases from the following text. Return ONLY a comma-separated list of keywords, nothing else:\n\n{text}"
            }
        ]
        
        # Use Meta Llama 3.1 - reliable and fast
        response = client.chat_completion(
            messages=messages,
            model="meta-llama/Llama-3.1-8B-Instruct",
            max_tokens=100,
            temperature=0.5
        )
        
        if response and hasattr(response, 'choices') and len(response.choices) > 0:
            keywords_text = response.choices[0].message.content.strip()
            # Split by comma and clean up
            keywords = [kw.strip().strip('"').strip("'") for kw in keywords_text.split(',')]
            keywords = [kw for kw in keywords if kw]  # Remove empty strings
            
            print(f"Extracted {len(keywords)} keywords")
            return keywords
        
        print("No keywords extracted")
        return []
        
    except Exception as e:
        print(f"Error in extract_keywords: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return []