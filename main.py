from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import base64
import tempfile
import pandas as pd

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

    # TODO: replace this with real Whisper transcription output
    # Example placeholder dataframe for one-column case
    df = pd.DataFrame({"소득": [100]})

    numeric_df = df.select_dtypes(include="number")

    result = {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "mean": numeric_df.mean().to_dict(),
        "std": numeric_df.std().to_dict(),
        "variance": numeric_df.var().to_dict(),
        "min": numeric_df.min().to_dict(),
        "max": numeric_df.max().to_dict(),
        "median": numeric_df.median().to_dict(),
        "mode": {col: numeric_df[col].mode().iloc[0] if not numeric_df[col].mode().empty else None for col in numeric_df.columns},
        "range": (numeric_df.max() - numeric_df.min()).to_dict(),
        "allowed_values": {},
        "value_range": {col: [numeric_df[col].min(), numeric_df[col].max()] for col in numeric_df.columns},
        "correlation": numeric_df.corr().fillna(0).values.tolist() if numeric_df.shape[1] > 1 else []
    }

    return JSONResponse(content=result)
