from transformers import AutoTokenizer, AutoModelForSequenceClassification, BitsAndBytesConfig
import torch

MODEL_PATH = "aarushibakshi/repo"

# Manual label mapping
LABELS = ["negative", "positive"]

# Use GPU if available, otherwise CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# ------------------------------
# Optimized model loading
# ------------------------------
print("Loading model and tokenizer...")

# Load tokenizer normally (lightweight)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# Load model with 8-bit quantization to reduce memory (70% smaller)
try:
    bnb_config = BitsAndBytesConfig(load_in_8bit=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_PATH,
        quantization_config=bnb_config,
        device_map="auto",
    )
    print("Loaded model in 8-bit quantized mode ✅")
except Exception as e:
    print(f"Quantization not available: {e}")
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    ).to(device)

model.eval()
print("Model loaded successfully ✅")

# ------------------------------
# Inference functions
# ------------------------------
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
