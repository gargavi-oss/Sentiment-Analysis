from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_PATH = "distilbert-sentiment" 

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()
model.to("cpu")

LABELS = ["negative", "positive"]

def analyze_sentiment(text: str):
    text = text.strip()
    if not text:
        return {"error": "Empty text provided."}
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
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
    results = []
    for t in texts:
        results.append(analyze_sentiment(t))
    return {"results": results}
