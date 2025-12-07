import os
from huggingface_hub import InferenceClient

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def summarize_text(text):
    """
    Summarize text using a chat model
    Using meta-llama model which is reliable and fast
    """
    try:
        print(f"Starting summarization for text of length: {len(text)}")
        
        # Truncate if too long
        max_length = 1024
        if len(text) > max_length:
            text = text[:max_length]
            print(f"Text truncated to {max_length} characters")
        
        # Create InferenceClient with the NEW base URL
        client = InferenceClient(
            token=HUGGINGFACE_API_KEY,
            base_url="https://router.huggingface.co"
        )
        
        # Use chat completion with a prompt to summarize
        messages = [
            {
                "role": "user",
                "content": f"Summarize the following text in 2-3 concise sentences. Only return the summary, nothing else:\n\n{text}"
            }
        ]
        
        # Use Meta Llama 3.1 - reliable and fast
        response = client.chat_completion(
            messages=messages,
            model="meta-llama/Llama-3.1-8B-Instruct",
            max_tokens=200,
            temperature=0.7
        )
        
        print(f"Response type: {type(response)}")
        
        if response and hasattr(response, 'choices') and len(response.choices) > 0:
            summary = response.choices[0].message.content.strip()
            if summary:
                print(f"Summary generated: {summary[:50]}...")
                return summary
        
        print("Could not generate summary")
        return "Summary unavailable"
        
    except Exception as e:
        print(f"Error in summarize_text: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return "Summary unavailable"