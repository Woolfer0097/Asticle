import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect, text

from app.handlers.health import router as health_router
from app.handlers.auth import router as auth_router
from app.handlers.article import router as tank_router
from app.handlers.users import router as users_router
from app.handlers.favourites import router as favourites_router
from app.config.config import get_settings
from app.database import Base, engine

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def ensure_article_owner_column() -> None:
    inspector = inspect(engine)
    columns = {column["name"] for column in inspector.get_columns("articles")}

    if "owner_id" in columns:
        return

    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE articles ADD COLUMN owner_id INTEGER"))


ensure_article_owner_column()

app.include_router(auth_router)
app.include_router(health_router)
app.include_router(tank_router)
app.include_router(users_router)
app.include_router(favourites_router)

# Mount для получения картинок сохраненных локально
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media"

MEDIA_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")


@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} is running",
    }
