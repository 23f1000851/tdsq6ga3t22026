from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import base64
import tempfile
import os
import pandas as pd
import numpy as np

app = FastAPI()

class AudioRequest(BaseModel):
    audio_id: str
    audio_base64: str


def clean_dict(d):
    out = {}
    for k, v in d.items():
        if pd.isna(v):
            out[k] = None
        elif isinstance(v, (np.integer, int)):
            out[k] = int(v)
        else:
            out[k] = float(v)
    return out


@app.get("/")
def home():
    return {"message": "API is running"}


@app.post("/predict")
def predict(req: AudioRequest):

    # Decode and save audio
    audio_bytes = base64.b64decode(req.audio_base64)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(audio_bytes)
        audio_path = f.name

    try:
        # =====================================================
        # TODO:
        # Replace this section with your speech-to-text +
        # table extraction logic.
        #
        # This DataFrame must be created from the AUDIO.
        # =====================================================
        df = pd.DataFrame({
            "소득": [40000, 42000, 45000, 45000, 48000]
        })
        # =====================================================

        numeric = df.select_dtypes(include="number")

        result = {
            "rows": int(len(df)),
            "columns": list(df.columns),
            "mean": clean_dict(numeric.mean().to_dict()),
            "std": clean_dict(numeric.std().to_dict()),
            "variance": clean_dict(numeric.var().to_dict()),
            "min": clean_dict(numeric.min().to_dict()),
            "max": clean_dict(numeric.max().to_dict()),
            "median": clean_dict(numeric.median().to_dict()),
            "mode": {
                c: numeric[c].mode().iloc[0]
                if not numeric[c].mode().empty
                else None
                for c in numeric.columns
            },
            "range": clean_dict((numeric.max() - numeric.min()).to_dict()),
            "allowed_values": {},
            "value_range": {
                c: [
                    float(numeric[c].min()),
                    float(numeric[c].max())
                ]
                for c in numeric.columns
            },
            "correlation": (
                numeric.corr().fillna(0).values.tolist()
                if numeric.shape[1] > 1
                else []
            ),
        }

        return JSONResponse(content=result)

    finally:
        os.remove(audio_path)
