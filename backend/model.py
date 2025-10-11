import joblib
import re

# Load your trained Logistic Regression model and TF-IDF vectorizer
lr_model = joblib.load("./model/sentiment_model.pkl")
vectorizer = joblib.load("./model/tfidf_vectorizer.pkl") # your saved TF-IDF vectorizer

# Same cleaning function used during training
def clean_text(text):
    stopwordlist = set([
        'a','about','above','after','again','all','am','an','and','any','are','as','at','be','because','been',
        'before','being','below','between','both','by','can','did','do','does','doing','down','during','each',
        'few','for','from','further','had','has','have','he','her','here','hers','him','his','how','i','if',
        'in','into','is','it','its','itself','just','me','more','most','my','myself','no','nor','not','of','on',
        'once','only','or','other','our','ours','out','own','re','s','she','so','some','such','t','than','that',
        'the','their','them','then','there','these','they','this','those','to','too','under','until','up','very',
        'was','we','were','what','when','where','which','while','who','why','will','with','you','your','yours',
        'yourself'
    ])
    text = text.lower()
    text = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', ' ', text)
    text = re.sub(r'@[\S]+', 'USER', text)
    text = re.sub(r'#(\S+)', r'\1', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = " ".join([w for w in text.split() if w not in stopwordlist])
    return text

# Labels
LABELS = ["negative", "neutral", "positive"]
EMOJIS = {"positive": "😊", "neutral": "😐", "negative": "😞"}

# ---------- Single text inference ----------
def analyze_sentiment(text: str, neutral_threshold=(0.4, 0.6)):
    text = text.strip()
    if not text:
        return {"error": "Empty text provided."}
    
    cleaned_text = clean_text(text)
    vect_text = vectorizer.transform([cleaned_text])
    
    # Get predicted probabilities
    probs = lr_model.predict_proba(vect_text)[0]
    
    # Determine class using threshold
    pos_prob = probs[1]
    neg_prob = probs[0]
    if pos_prob >= neutral_threshold[1]:
        label = "positive"
    elif neg_prob >= neutral_threshold[1]:
        label = "negative"
    else:
        label = "neutral"
    
    score = max(probs)  # confidence score
    return {"text": text, "label": label, "score": round(score, 3), "emoji": EMOJIS[label]}

# ---------- Batch inference ----------
def analyze_batch(texts: list[str], neutral_threshold=(0.4, 0.6)):
    texts = [t.strip() for t in texts if t.strip()]
    if not texts:
        return {"results": []}
    
    cleaned_texts = [clean_text(t) for t in texts]
    vect_texts = vectorizer.transform(cleaned_texts)
    probs_list = lr_model.predict_proba(vect_texts)
    
    results = []
    for i, text in enumerate(texts):
        probs = probs_list[i]
        pos_prob = probs[1]
        neg_prob = probs[0]
        if pos_prob >= neutral_threshold[1]:
            label = "positive"
        elif neg_prob >= neutral_threshold[1]:
            label = "negative"
        else:
            label = "neutral"
        score = max(probs)
        results.append({"text": text, "label": label, "score": round(score,3), "emoji": EMOJIS[label]})
    
    return {"results": results}

# ---------- Test ----------
if __name__ == "__main__":
    print(analyze_sentiment("I am happy but also hurt."))
    print(analyze_batch([
        "I love this product!",
        "This is terrible!",
        "I’m okay with it, not too bad."
    ]))
