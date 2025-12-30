## Run locally (venv)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload

## Environment variables

This API supports authenticated Hugging Face requests.

Set your token locally:
```bash
export HF_API_TOKEN="your_token"
uvicorn app.main:app --reload
