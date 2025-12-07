import os
from huggingface_hub import InferenceClient

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def extract_keywords(text):
    """
    Extract keywords using Keyphrase Extraction via Inference Providers
    Model: ml6team/keyphrase-extraction-kbir-inspec
    """
    try:
        print(f"Starting keyword extraction for text of length: {len(text)}")
        
        # Truncate if too long
        max_length = 512
        if len(text) > max_length:
            text = text[:max_length]
        
        # Create InferenceClient
        client = InferenceClient(token=HUGGINGFACE_API_KEY)
        
        # Use token_classification for keyphrase extraction
        result = client.token_classification(
            text=text,
            model="ml6team/keyphrase-extraction-kbir-inspec"
        )
        
        if result:
            keywords = set()
            for item in result:
                if isinstance(item, dict) and "word" in item:
                    keyword = item["word"].strip()
                    # Clean up subword tokens
                    keyword = keyword.replace("##", "")
                    if keyword:
                        keywords.add(keyword)
            
            keyword_list = list(keywords)
            print(f"Extracted {len(keyword_list)} keywords")
            return keyword_list
        
        print("No result from API")
        return []
        
    except Exception as e:
        print(f"Error in extract_keywords: {type(e).__name__}: {str(e)}")
        return []