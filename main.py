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
            "rows": 0,
            "columns": [],
            "mean": {},
            "std": {},
            "variance": {},
            "min": {},
            "max": {},
            "median": {},
            "mode": {},
            "range": {},
            "allowed_values": {},
            "value_range": {},
            "correlation": []
        }
    )
