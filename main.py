from fastapi import FastAPI, Request, HTTPException
import base64
import traceback

app = FastAPI()

@app.post("/predict")
async def solve(req: Request):
    try:
        data = await req.json()

        audio_b64 = data.get("audio_base64")
        if not audio_b64:
            raise HTTPException(status_code=400, detail="audio_base64 missing")

        audio_bytes = base64.b64decode(audio_b64)

        with open("/tmp/temp.wav", "wb") as f:
            f.write(audio_bytes)

        return {
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

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
