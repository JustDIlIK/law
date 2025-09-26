import os
from pathlib import Path
from uuid import uuid4

import httpx


async def download_image(url: str, save_path: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        Path(save_path).write_bytes(resp.content)


async def save_image(file, url):
    file_name = f"{uuid4().hex}.{file.filename.split(".")[-1]}"

    file_name = file_name.replace(" ", "")

    file_path = os.path.join(url, file_name)

    Path(url).mkdir(parents=True, exist_ok=True)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return file_path
