from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@patch("app.main.hf.infer", new_callable=AsyncMock)
def test_sentiment(mock_infer):
    mock_infer.return_value = [{"label": "POSITIVE", "score": 0.99}]
    r = client.post("/ai/sentiment", json={"text": "I love this product"})
    assert r.status_code == 200
    assert r.json()["label"] == "POSITIVE"


@patch("app.main.hf.infer", new_callable=AsyncMock)
def test_summarize(mock_infer):
    mock_infer.return_value = [{"summary_text": "Short summary."}]
    r = client.post("/ai/summarize", json={"text": "Long text..."})
    assert r.status_code == 200
    assert r.json()["summary"] == "Short summary."
