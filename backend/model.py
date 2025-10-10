from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Your Hugging Face model repo or local path
MODEL_PATH = "twitter_sentiment_model"

# Manual label mapping (match training)
LABELS = ["negative", "positive"]

# Load model + tokenizer once (at startup)
print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# Automatically choose device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load model in optimized dtype
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
)
model.to(device)
model.eval()

# ---------- Single text inference ----------
def analyze_sentiment(text: str):
    text = text.strip()
    if not text:
        return {"error": "Empty text provided."}

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128).to(device)
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

# ---------- Batch inference ----------
def analyze_batch(texts: list[str]):
    texts = [t.strip() for t in texts if t.strip()]
    if not texts:
        return {"results": []}

    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=128).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

    results = []
    for i, text in enumerate(texts):
        pred_idx = torch.argmax(probs[i]).item()
        score = probs[i][pred_idx].item()
        results.append({
            "text": text,
            "label": LABELS[pred_idx],
            "score": round(score, 3),
            "emoji": "😊" if LABELS[pred_idx] == "positive" else "😞"
        })

    return {"results": results}


# ---------- Test locally ----------
if __name__ == "__main__":
    print(analyze_sentiment("I love this product!"))
    print(analyze_batch(["I love this!", "This is bad.", "So-so experience"]))
