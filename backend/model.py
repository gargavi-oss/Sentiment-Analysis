import requests
import os

# Replace with your model repo ID
MODEL_ID = "aarushibakshi/repo"

# Add your token (you can store it as an environment variable in Render)
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}


def analyze_sentiment(text: str):
    text = text.strip()
    if not text:
        return {"error": "Empty text provided."}

    payload = {"inputs": text}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    result = response.json()

    try:
        label = result[0][0]["label"].lower()
        score = round(result[0][0]["score"], 3)
        return {
            "text": text,
            "label": label,
            "score": score,
            "emoji": "😊" if "pos" in label else "😞"
        }
    except Exception as e:
        return {"error": str(result)}


def analyze_batch(texts: list[str]):
    texts = [t.strip() for t in texts if t.strip()]
    if not texts:
        return {"results": []}

    payload = {"inputs": texts}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    result = response.json()

    results = []
    try:
        for i, res in enumerate(result):
            label = res[0]["label"].lower()
            score = round(res[0]["score"], 3)
            results.append({
                "text": texts[i],
                "label": label,
                "score": score,
                "emoji": "😊" if "pos" in label else "😞"
            })
    except Exception as e:
        return {"error": str(result)}

    return {"results": results}
