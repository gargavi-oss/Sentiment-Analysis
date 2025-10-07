from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_PATH = "twitter_sentiment_model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
labels = ["negative", "positive"]

def analyze_sentiment(text: str):
    if not text.strip():
        return {"error": "Empty text provided."}
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    pred = torch.argmax(probs, dim=1).item()
    score = round(probs[0][pred].item(), 3)
    label = labels[pred]
    return {"label": label, "score": score}

if __name__ == "__main__":
    while True:
        text = input("\nEnter text (or type 'exit' to quit): ")
        if text.lower() == "exit":
            break
        result = analyze_sentiment(text)
        print(result)
