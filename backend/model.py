from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_PATH = "twitter_sentiment_model"

# Load model and tokenizer
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Error loading model from {MODEL_PATH}: {e}")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# Adjust labels according to your fine-tuned model
labels = ["negative", "positive"]

def analyze_sentiment(text: str):
    """Single text sentiment analysis"""
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

    pred = torch.argmax(probs, dim=1).item()
    score = round(probs[0][pred].item(), 3)
    label = labels[pred] if pred < len(labels) else "unknown"

    return {
        "text": text,
        "label": label,
        "score": score,
        "emoji": "😊" if label == "positive" else "😞" if label == "negative" else "😐"
    }


def analyze_batch(texts: list[str]):
    """Batch sentiment analysis for multiple texts"""
    # Remove empty strings
    texts = [t.strip() for t in texts if t.strip()]
    if not texts:
        return {"results": []}  # Return empty list instead of single summary

    # Tokenize all texts
    inputs = tokenizer(
        texts,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

    preds = torch.argmax(probs, dim=1)

    results = []
    for i, text in enumerate(texts):
        label = labels[preds[i].item()] if preds[i].item() < len(labels) else "unknown"
        score = round(probs[i][preds[i]].item(), 3)
        results.append({
            "text": text,
            "label": label,
            "score": score,
            "emoji": "😊" if label == "positive" else "😞" if label == "negative" else "😐"
        })

    # Return as an array of individual results
    return {"results": results}
