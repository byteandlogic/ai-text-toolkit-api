from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.hf_client import HFClient, DEFAULT_SENTIMENT_MODEL, DEFAULT_SUMMARY_MODEL

app = FastAPI(title="AI Text Toolkit API")
hf = HFClient()


class TextIn(BaseModel):
    text: str


class SentimentOut(BaseModel):
    label: str
    score: float
    model: str


class SummaryOut(BaseModel):
    summary: str
    model: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ai/sentiment", response_model=SentimentOut)
async def sentiment(body: TextIn):
    data = await hf.infer(DEFAULT_SENTIMENT_MODEL, {"inputs": body.text})
    if isinstance(data, dict) and data.get("error"):
        raise HTTPException(status_code=502, detail=data)

    top = sorted(data, key=lambda x: x["score"], reverse=True)[0]
    return {"label": top["label"], "score": float(top["score"]), "model": DEFAULT_SENTIMENT_MODEL}


@app.post("/ai/summarize", response_model=SummaryOut)
async def summarize(body: TextIn):
    data = await hf.infer(DEFAULT_SUMMARY_MODEL, {"inputs": body.text})
    if isinstance(data, dict) and data.get("error"):
        raise HTTPException(status_code=502, detail=data)

    summary_text = data[0].get("summary_text") if isinstance(data, list) and data else None
    if not summary_text:
        raise HTTPException(status_code=502, detail="Unexpected upstream response")
    return {"summary": summary_text, "model": DEFAULT_SUMMARY_MODEL}
