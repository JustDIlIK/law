import os
from pathlib import Path
from uuid import uuid4

import httpx

from app.config.config import BASE_DIR


async def download_image(url: str, save_path: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

        relative_path = save_path.lstrip("/")
        file_path = os.path.join(BASE_DIR, relative_path)
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        Path(file_path).write_bytes(resp.content)


async def save_image(file, url: str):
    file_name = f"{uuid4().hex}.{file.filename.split('.')[-1]}".replace(" ", "")

    save_dir = os.path.join(BASE_DIR, url)
    file_path = os.path.join(save_dir, file_name)

    Path(save_dir).mkdir(parents=True, exist_ok=True)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return os.path.relpath(file_path, BASE_DIR)
