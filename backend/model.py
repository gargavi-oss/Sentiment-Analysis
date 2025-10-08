from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Replace this with either a local path or Hugging Face model repo ID
# Use HF Hub or local path
MODEL_PATH = "aarushibakshi/repo"

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# Define labels explicitly (override numeric labels)
# Adjust based on your fine-tuned model
labels = ["negative", "positive"]

def analyze_sentiment(text: str):
    text = text.strip()
    if not text:
        return {"error": "Empty text provided."}

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

    pred = torch.argmax(probs, dim=1).item()
    score = round(probs[0][pred].item(), 3)
    label = labels[pred]  # use the mapped label

    return {
        "text": text,
        "label": label,
        "score": score,
        "emoji": "😊" if label == "positive" else "😞"
    }


def analyze_batch(texts: list[str]):
    texts = [t.strip() for t in texts if t.strip()]
    if not texts:
        return {"results": []}

    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=128).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

    preds = torch.argmax(probs, dim=1)
    results = []
    for i, text in enumerate(texts):
        label = labels[preds[i].item()]  # map numeric label to string
        score = round(probs[i][preds[i]].item(), 3)
        results.append({
            "text": text,
            "label": label,
            "score": score,
            "emoji": "😊" if label == "positive" else "😞"
        })

    return {"results": results}
