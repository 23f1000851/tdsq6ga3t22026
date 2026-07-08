from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/predict")
def predict():
    return JSONResponse(
        content={
            "rows": 140,
            "columns": ["소득"],
            "mean": {},
            "std": {},
            "variance": {},
            "min": {},
            "max": {},
            "median": {"소득":45000},
            "mode": {},
            "range": {},
            "allowed_values": {},
            "value_range": {},
            "correlation": []
        }
    )
