from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.favourite import FavouriteResponse
from app.services.favourite_service import FavouriteService
from app.models.user import User

from app.auth import get_current_user

router = APIRouter(
    prefix="/favourites",
    tags=["favourites"],
)


def get_favourite_service(db: Session = Depends(get_db)) -> FavouriteService:
    return FavouriteService(db)


@router.get("/", response_model=list[FavouriteResponse])
def get_favourites(
    current_user: User = Depends(get_current_user),
    service: FavouriteService = Depends(get_favourite_service),
):
    return service.get_favourites_by_user_id(current_user.id)


@router.post(
    "/{article_id}",
    response_model=FavouriteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_favourite(
    article_id: int,
    current_user: User = Depends(get_current_user),
    service: FavouriteService = Depends(get_favourite_service),
):
    return service.create_favourite(article_id, current_user.id)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favourite(
    article_id: int,
    current_user: User = Depends(get_current_user),
    service: FavouriteService = Depends(get_favourite_service),
) -> None:
    service.delete_favourite(article_id, current_user.id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_favourites_from_user(
    current_user: User = Depends(get_current_user),
    service: FavouriteService = Depends(get_favourite_service),
):
    service.delete_all_favourites_from_user(current_user.id)
