import os
from huggingface_hub import InferenceClient

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def summarize_text(text):
    """
    Summarize text using BART Large CNN via Inference Providers
    Model: facebook/bart-large-cnn
    """
    try:
        print(f"Starting summarization for text of length: {len(text)}")
        
        # Truncate if too long
        max_length = 1024
        if len(text) > max_length:
            text = text[:max_length]
            print(f"Text truncated to {max_length} characters")
        
        # Create InferenceClient
        client = InferenceClient(token=HUGGINGFACE_API_KEY)
        
        # Use summarization method - removed invalid parameters
        # InferenceClient.summarization() doesn't accept max_length/min_length directly
        result = client.summarization(
            text=text,
            model="facebook/bart-large-cnn"
        )
        
        if result and hasattr(result, 'summary_text'):
            summary = result.summary_text
            print(f"Summary generated: {summary[:50]}...")
            return summary
        elif isinstance(result, dict) and 'summary_text' in result:
            summary = result['summary_text']
            print(f"Summary generated: {summary[:50]}...")
            return summary
        
        print("Could not extract summary from response")
        return "Summary unavailable"
        
    except Exception as e:
        print(f"Error in summarize_text: {type(e).__name__}: {str(e)}")
        return "Summary unavailable"