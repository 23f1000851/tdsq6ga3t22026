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


@app.post("/predict")
def predict(req: AudioRequest):
    try:
        audio_bytes = base64.b64decode(req.audio_base64)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes)
            temp_path = f.name

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
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
