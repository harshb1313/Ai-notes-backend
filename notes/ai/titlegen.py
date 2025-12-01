import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)  # <---- IMPORTANT

def createTitle(text):
    prompt = "generate title: " + text
    encoding = tokenizer.encode_plus(
        prompt,
        padding="max_length",
        max_length=256,
        return_tensors="pt",
        truncation=True
    )

    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)

    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        do_sample=True,
        max_length=128,
        top_k=60,
        top_p=0.9,
        early_stopping=True,
        num_return_sequences=1
    )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
