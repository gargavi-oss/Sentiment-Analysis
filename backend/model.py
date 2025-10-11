import joblib
import re

# ---------------- Load Model, Vectorizer, and Label Encoder ----------------
model = joblib.load('./model/logreg_sentiment_model.pkl')
vectorizer = joblib.load('./model/tfidf_vectorizer.pkl')
label_encoder = joblib.load('./model/label_encoder.pkl')

# ---------------- Text Cleaning ----------------
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ---------------- Labels and Emojis ----------------
EMOJIS = {"negative": "😞", "neutral": "😐", "positive": "😊"}

# ---------------- Rule-based override ----------------
POSITIVE_WORDS = {"happy","love","great","good","awesome","fantastic","amazing"}
NEGATIVE_WORDS = {"injured","bad","worst","sad","terrible","pain","hurt"}

def apply_neutral_rule(text, predicted_label):
    text_words = set(preprocess_text(text).split())
    if any(w in text_words for w in POSITIVE_WORDS) and any(w in text_words for w in NEGATIVE_WORDS):
        return "neutral"
    return predicted_label

# ---------------- Single Tweet Analysis ----------------
def analyze_sentiment(text):
    text = text.strip()
    if not text:
        return {"error": "Empty text provided."}

    cleaned_text = preprocess_text(text)
    vect_text = vectorizer.transform([cleaned_text])

    pred_class = model.predict(vect_text)[0]
    pred_label = label_encoder.inverse_transform([pred_class])[0]

    # Apply rule-based neutral override
    pred_label = apply_neutral_rule(text, pred_label)

    pred_proba = model.predict_proba(vect_text)[0].max()

    return {
        "text": text,
        "label": pred_label,
        "score": round(pred_proba, 3),
        "emoji": EMOJIS.get(pred_label, "😐")
    }

# ---------------- Batch Analysis ----------------
def analyze_batch(texts):
    texts = [t.strip() for t in texts if t.strip()]
    if not texts:
        return {"results": []}

    cleaned_texts = [preprocess_text(t) for t in texts]
    vect_texts = vectorizer.transform(cleaned_texts)
    pred_classes = model.predict(vect_texts)
    pred_probs = model.predict_proba(vect_texts)

    results = []
    for i, text in enumerate(texts):
        label = label_encoder.inverse_transform([pred_classes[i]])[0]

        # Apply rule-based neutral override
        label = apply_neutral_rule(text, label)

        score = pred_probs[i].max()
        results.append({
            "text": text,
            "label": label,
            "score": round(score, 3),
            "emoji": EMOJIS.get(label, "😐")
        })
    return {"results": results}

# ---------------- Example ----------------
if __name__ == "__main__":
    text = "I am happy that I am injured"
    print(analyze_sentiment(text))
