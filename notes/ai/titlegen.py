import os
from huggingface_hub import InferenceClient

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def createTitle(text):
    """
    Generate title using a chat model
    Using meta-llama model which is reliable and fast
    """
    try:
        print(f"\n=== TITLE GENERATION START ===")
        print(f"Input text length: {len(text)}")
        print(f"API Key present: {bool(HUGGINGFACE_API_KEY)}")
        
        # Truncate text to reasonable length
        text_snippet = text[:500] if len(text) > 500 else text
        print(f"Text snippet: {text_snippet[:100]}...")
        
        # Create InferenceClient with the NEW base URL
        client = InferenceClient(
            token=HUGGINGFACE_API_KEY,
            base_url="https://router.huggingface.co"
        )
        
        # Use chat completion with a prompt to generate title
        messages = [
            {
                "role": "user",
                "content": f"Generate a short, concise title (5-10 words maximum) for this text. Only return the title, nothing else:\n\n{text_snippet}"
            }
        ]
        
        # Use Meta Llama 3.1 - reliable and fast
        response = client.chat_completion(
            messages=messages,
            model="meta-llama/Llama-3.1-8B-Instruct",
            max_tokens=50,
            temperature=0.7
        )
        
        print(f"Response type: {type(response)}")
        
        if response and hasattr(response, 'choices') and len(response.choices) > 0:
            title = response.choices[0].message.content.strip()
            # Clean up the title (remove quotes if present)
            title = title.strip('"').strip("'")
            if title:
                print(f"✓ Generated title: {title}")
                print(f"=== TITLE GENERATION END ===\n")
                return title
        
        print("No title generated - returning 'Untitled'")
        print(f"=== TITLE GENERATION END ===\n")
        return "Untitled"
        
    except Exception as e:
        print(f"!!! Error in createTitle: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"=== TITLE GENERATION END ===\n")
        return "Untitled"