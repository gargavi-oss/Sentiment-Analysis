from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model import analyze_sentiment, analyze_batch

app = FastAPI(title="Twitter Sentiment Analysis API")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

class BatchRequest(BaseModel):
    texts: list[str]

@app.get("/")
async def root():
    return {"message": "Welcome to Twitter Sentiment Analysis API 🚀"}

@app.post("/analyze")
async def analyze_text(data: TextRequest):
    try:
        return analyze_sentiment(data.text)
    except Exception as e:
        return {"error": str(e)}

@app.post("/batch_analyze")
async def analyze_batch_texts(data: BatchRequest):
    try:
        return analyze_batch(data.texts)
    except Exception as e:
        return {"error": str(e)}
