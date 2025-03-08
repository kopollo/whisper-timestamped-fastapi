import asyncio
import httpx
import os
import time
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
API_URL = "http://localhost:8000/transcribe"  # Замените на ваш URL
AUDIO_FILE = "audio_sample.mp3"  # Путь к аудиофайлу для тестирования
TOTAL_REQUESTS = 100  # Общее количество запросов для тестирования
REQUESTS_PER_SECOND = 5  # Количество запросов в секунду
TIMEOUT_SECONDS = 10  # Увеличенный таймаут в секундах

# Ограничение на количество одновременно выполняемых запросов
# semaphore = asyncio.Semaphore(REQUESTS_PER_SECOND)

async def send_request(client: httpx.AsyncClient):
    # async with semaphore:
    with open(AUDIO_FILE, "rb") as f:
        files = {"file": (os.path.basename(AUDIO_FILE), f, "audio/mpeg")}
        response = await client.post(API_URL, files=files, timeout=20)
        return response

async def load_test():
    # timeout = httpx.(TIMEOUT_SECONDS)  # Установка таймаута
    async with httpx.AsyncClient() as client:
        tasks = []
        for _ in range(TOTAL_REQUESTS):
            tasks.append(send_request(client))
            # Задержка для соблюдения лимита запросов в секунду
            if len(tasks) % REQUESTS_PER_SECOND == 0:
                await asyncio.sleep(1)  # Ждем 1 секунду

        responses = await asyncio.gather(*tasks)
        return responses

def main():
    start_time = time.time()
    responses = asyncio.run(load_test())
    end_time = time.time()

    for response in responses:
        print(f"Response status: {response.status_code}, Response: {response.json()}")

    print(f"Total time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
