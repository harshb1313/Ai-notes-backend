import os
from huggingface_hub import InferenceClient

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def createTitle(text):
    """
    Generate title using a chat model via OpenAI-compatible endpoint
    Using Qwen model which is fast and free
    """
    try:
        print(f"\n=== TITLE GENERATION START ===")
        print(f"Input text length: {len(text)}")
        print(f"API Key present: {bool(HUGGINGFACE_API_KEY)}")
        
        # Truncate text to reasonable length
        text_snippet = text[:500] if len(text) > 500 else text
        print(f"Text snippet: {text_snippet[:100]}...")
        
        # Create InferenceClient
        client = InferenceClient(api_key=HUGGINGFACE_API_KEY)
        
        # Use chat completion with a prompt to generate title
        messages = [
            {
                "role": "user",
                "content": f"Generate a short, concise title (5-10 words maximum) for this text. Only return the title, nothing else:\n\n{text_snippet}"
            }
        ]
        
        # Use a fast, free model via the chat completion endpoint
        response = client.chat_completion(
            messages=messages,
            model="Qwen/Qwen2.5-Coder-32B-Instruct",  # Fast and free model
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