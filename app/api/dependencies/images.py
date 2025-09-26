from fastapi import UploadFile, File, HTTPException


def check_image(file: UploadFile = File(None)):

    if file and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Загрузите изображение")

    return file
