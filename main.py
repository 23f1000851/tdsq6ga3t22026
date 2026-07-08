from fastapi import FastAPI, HTTPException
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


@app.post("/predict")
def predict(req: AudioRequest):
    temp_path = None

    try:
        # Decode audio
        audio_bytes = base64.b64decode(req.audio_base64)

        # Save temporary wav file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes)
            temp_path = f.name

        ##################################################
        # Replace this with your Whisper transcription
        ##################################################
        df = pd.DataFrame({
            "소득": [100]
        })
        ##################################################

        numeric_df = df.select_dtypes(include=[np.number])

        def clean_dict(d):
            result = {}
            for k, v in d.items():
                if pd.isna(v):
                    result[k] = None
                else:
                    result[k] = float(v) if isinstance(v, (np.floating, float)) else int(v)
            return result

        if numeric_df.empty:
            response = {
                "rows": len(df),
                "columns": list(df.columns),
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
            return JSONResponse(content=response)

        mode_dict = {}
        for col in numeric_df.columns:
            m = numeric_df[col].mode()
            if len(m):
                val = m.iloc[0]
                mode_dict[col] = float(val) if isinstance(val, (np.floating, float)) else int(val)
            else:
                mode_dict[col] = None

        corr = numeric_df.corr().fillna(0)

        response = {
            "rows": int(len(df)),
            "columns": list(df.columns),
            "mean": clean_dict(numeric_df.mean().to_dict()),
            "std": clean_dict(numeric_df.std().to_dict()),
            "variance": clean_dict(numeric_df.var().to_dict()),
            "min": clean_dict(numeric_df.min().to_dict()),
            "max": clean_dict(numeric_df.max().to_dict()),
            "median": clean_dict(numeric_df.median().to_dict()),
            "mode": mode_dict,
            "range": clean_dict((numeric_df.max() - numeric_df.min()).to_dict()),
            "allowed_values": {},
            "value_range": {
                col: [
                    float(numeric_df[col].min()),
                    float(numeric_df[col].max())
                ]
                for col in numeric_df.columns
            },
            "correlation": corr.values.tolist() if numeric_df.shape[1] > 1 else []
        }

        return JSONResponse(content=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
