## Run locally (venv)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
