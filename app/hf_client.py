import os
import httpx

HF_API = "https://api-inference.huggingface.co/models"

DEFAULT_SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
DEFAULT_SUMMARY_MODEL = "facebook/bart-large-cnn"


class HFClient:
    def __init__(self, token: str | None = None):
        self.token = token or os.getenv("HF_TOKEN", "")
        self.headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}

    async def infer(self, model: str, payload: dict) -> dict:
        url = f"{HF_API}/{model}"
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(url, headers=self.headers, json=payload)

        if r.status_code >= 400:
            return {"error": f"Upstream error {r.status_code}", "details": r.text}

        return r.json()
