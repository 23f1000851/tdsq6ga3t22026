from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import base64
import tempfile

app = FastAPI()


class AudioRequest(BaseModel):
    audio_id: str
    audio_base64: str


@app.get("/")
def home():
    return {"status": "ok"}


@app.get("/predict")
def predict():
    return JSONResponse(content={
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
    })
