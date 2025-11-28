import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load once when server starts
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = T5Tokenizer.from_pretrained("ramsrigouthamg/t5_paraphraser")
model = T5ForConditionalGeneration.from_pretrained("ramsrigouthamg/t5_paraphraser").to(device)

def paraphrase_text(text):
    input_text = "paraphrase: " + text + " </s>"

    encoding = tokenizer.encode_plus(
        input_text,
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
        max_length=256,
        top_k=120,
        top_p=0.98,
        early_stopping=True,
        num_return_sequences=1   # only 1 para needed
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
