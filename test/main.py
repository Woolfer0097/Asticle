import os
from pathlib import Path
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.staticfiles import StaticFiles

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media"
TANK_IMAGES_DIR = MEDIA_DIR / "tanks"

# Directories must exist before StaticFiles is mounted
TANK_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/media",
    StaticFiles(directory=MEDIA_DIR),
    name="media",
)


@app.post("/images/upload")  # response_model=ImageUploadSchema
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
):
    filename = file.filename
    image_path = TANK_IMAGES_DIR / filename
    if os.path.exists(image_path):
        return HTTPException(
            status_code=400, detail="Изображение с таким названием уже существует"
        )

    content = await file.read()
    image_path.write_bytes(content)

    # with open(image_path, "wb") as f:
    #     f.write(file.file.read())

    image_url = request.url_for(
        "media",
        path=filename,
    )

    return {
        "filename": filename,
        "photo_path": f"/media/{filename}",
        "image_url": str(image_url),
    }
