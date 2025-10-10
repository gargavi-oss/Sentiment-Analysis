from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import time
import os

MODEL_PATH = "distilbert-sentiment"  # local folder for your distilled model
LABELS = ["negative", "positive"]


start_time = time.time()
print(f"🚀 Loading sentiment model from {MODEL_PATH} ...")


tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()
device = "mps" if torch.backends.mps.is_available() else "cpu" 
model.to(device)

load_time = round(time.time() - start_time, 2)
print(f"✅ Model loaded and cached in {load_time}s on {device.upper()}")

def analyze_sentiment(text: str):
    text = text.strip()
    if not text:
        return {"error": "Empty text provided."}

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

    pred_idx = torch.argmax(probs, dim=-1).item()
    score = probs[0][pred_idx].item()

    return {
        "text": text,
        "label": LABELS[pred_idx],
        "score": round(score, 3),
        "emoji": "😊" if LABELS[pred_idx] == "positive" else "😞"
    }


def analyze_batch(texts: list[str]):
    if not texts:
        return {"error": "Empty list provided."}

    results = [analyze_sentiment(t) for t in texts]
    return {"results": results}
