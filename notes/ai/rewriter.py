import os
from huggingface_hub import InferenceClient

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def paraphrase_text(text):
    """
    Paraphrase text using a chat model
    Using meta-llama model which is reliable and fast
    """
    try:
        print(f"\n=== PARAPHRASING START ===")
        print(f"Starting paraphrasing for text of length: {len(text)}")
        
        # Truncate if too long
        max_length = 800
        if len(text) > max_length:
            text = text[:max_length]
            print(f"Text truncated to {max_length} characters")
        
        # Create InferenceClient with the NEW base URL
        client = InferenceClient(
            token=HUGGINGFACE_API_KEY,
            base_url="https://router.huggingface.co"
        )
        
        # Use chat completion with a prompt to paraphrase
        messages = [
            {
                "role": "user",
                "content": f"Paraphrase the following text while keeping the same meaning. Only return the paraphrased text, nothing else:\n\n{text}"
            }
        ]
        
        # Use Meta Llama 3.1 - reliable and fast
        response = client.chat_completion(
            messages=messages,
            model="meta-llama/Llama-3.1-8B-Instruct",
            max_tokens=1000,
            temperature=0.7
        )
        
        print(f"Response type: {type(response)}")
        
        if response and hasattr(response, 'choices') and len(response.choices) > 0:
            paraphrased = response.choices[0].message.content.strip()
            if paraphrased:
                print(f"✓ Paraphrasing successful")
                print(f"Preview: {paraphrased[:100]}...")
                print(f"=== PARAPHRASING END ===\n")
                return paraphrased
        
        print("No paraphrase generated - returning original text")
        print(f"=== PARAPHRASING END ===\n")
        return text
        
    except Exception as e:
        print(f"!!! Error in paraphrase_text: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"=== PARAPHRASING END ===\n")
        return text