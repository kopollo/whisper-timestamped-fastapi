import os

import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

from config import cfg

app = FastAPI()

UPLOAD_DIR = "upload/audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

import whisper_timestamped

path = "files/test.wav"
model = whisper_timestamped.load_model(cfg['model'], device=cfg['device'])


async def process_audio(audio_path: str):
    try:
        audio = whisper_timestamped.load_audio(audio_path)
        result = whisper_timestamped.transcribe(model, audio)
        print(result)
    finally:
        os.remove(audio_path)  # Удаляем временный файл после обработки
    return result


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        print(file_path)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        result = await process_audio(file_path)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("client:app", host="0.0.0.0", port=8000, workers=3)
