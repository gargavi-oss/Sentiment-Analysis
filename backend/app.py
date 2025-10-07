from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model import analyze_sentiment  

app = FastAPI(title="Twitter Sentiment Analysis API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextRequest(BaseModel):
    text: str


@app.post("/analyze")
async def analyze_text(data: TextRequest):
    sentiment = analyze_sentiment(data.text)
    return sentiment

@app.get("/")
async def root():
    return {"message": "Welcome to Twitter Sentiment Analysis API"}
