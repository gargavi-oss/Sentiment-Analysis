from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model import analyze_sentiment, analyze_batch
import os
import uvicorn

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
    
if __name__ == "__main__":
    import os
    import uvicorn

    # Render dynamically assigns a port
    port = int(os.environ.get("PORT", 10000))

    # Bind FastAPI to that port
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
