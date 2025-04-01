import os
import traceback

import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

from config import cfg
import whisper_timestamped
from logging_config import init_logger

app = FastAPI()

UPLOAD_DIR = "upload/audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

model = whisper_timestamped.load_model(cfg['model'], device=cfg['device'], download_root='.cache')

logger = init_logger(__name__)


async def process_audio(audio_path: str, language):
    try:
        audio = whisper_timestamped.load_audio(audio_path)
        result = whisper_timestamped.transcribe(model, audio, language=language)
        logger.info(result)
    finally:
        os.remove(audio_path)  # Удаляем временный файл после обработки
    return result


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...), language="en"):
    logger.info(f"Got request! lang: {language}")
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        logger.info(f"Try to load file: {file_path}")
        with open(file_path, "wb") as f:
            f.write(await file.read())

        result = await process_audio(file_path, language)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error("An error occurred: %s", traceback.format_exc())
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("client:app", host="0.0.0.0", port=9000, workers=1)
