# JoSAA Predictor Backend

## Run locally
```bash
pip install -r requirements.txt
uvicorn predictor_backend:app --reload
```

## Deploy to Render
- Create a new Web Service
- Runtime: Python 3.11
- Start command: `uvicorn predictor_backend:app --host 0.0.0.0 --port 10000`
