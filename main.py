from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import base64
import tempfile

app = FastAPI()

class AudioRequest(BaseModel):
    audio_id: str
    audio_base64: str

@app.post("/predict")
def predict(req: AudioRequest):
    audio_bytes = base64.b64decode(req.audio_base64)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        audio_path = f.name

    # transcribe audio_path with Whisper
    # build output from transcription

    return JSONResponse(content={
        "rows": 0,
        "columns": ["소득"],
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
