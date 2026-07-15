import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, status, UploadFile
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.article import ArticleCreate, ArticleResponse, ArticleUpdate
from app.services.article_service import ArticleService

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
)

MEDIA_DIR = Path(__file__).resolve().parents[2] / "media"


def get_article_service(db: Session = Depends(get_db)) -> ArticleService:
    return ArticleService(db)


@router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def create_article(
    schema: ArticleCreate,
    service: ArticleService = Depends(get_article_service),
    current_user: User = Depends(get_current_user),
):
    return service.create_article(schema, current_user)


@router.get("/", response_model=list[ArticleResponse])
def get_articles(service: ArticleService = Depends(get_article_service)):
    return service.get_articles()


@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(
    article_id: int, service: ArticleService = Depends(get_article_service)
):
    return service.get_article(article_id)


@router.patch("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    schema: ArticleUpdate,
    service: ArticleService = Depends(get_article_service),
    current_user: User = Depends(get_current_user),
):
    return service.update_article(article_id, schema, current_user)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: int,
    service: ArticleService = Depends(get_article_service),
    current_user: User = Depends(get_current_user),
) -> None:
    service.delete_article(article_id, current_user)


@router.post("/{article_id}/photo", status_code=status.HTTP_201_CREATED)
async def load_photo(
    article_id: int,
    file: UploadFile = File(...),
    service: ArticleService = Depends(get_article_service),
    current_user: User = Depends(get_current_user),
):
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)

    extension = Path(file.filename or "").suffix
    filename = f"{uuid.uuid4()}{extension}"
    filepath = MEDIA_DIR / filename

    with open(filepath, "wb") as f:
        f.write(await file.read())

    return service.update_article(
        article_id,
        ArticleUpdate(cover_url=f"/media/{filename}"),
        current_user,
    )
