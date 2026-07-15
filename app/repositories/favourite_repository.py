from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.models.favourite import Favourite

from app.repositories.article_repository import ArticleRepository

from typing import Optional


class FavouriteRepository:
    def __init__(self, db: Session):
        self.db = db
        self.article_repository = ArticleRepository(db)

    def create(self, favourite: Favourite) -> Favourite:
        if not self.article_repository.get_by_id(favourite.article_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found",
            )

        try:
            self.db.add(favourite)
            self.db.commit()
            self.db.refresh(favourite)

            return favourite
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Article already exists",
            )

    def get_all_by_user_id(self, user_id: int) -> list[Favourite]:
        return self.db.query(Favourite).filter(Favourite.user_id == user_id).all()

    def delete(self, article_id: int, user_id: int) -> None:
        self.db.query(Favourite).filter(
            Favourite.article_id == article_id, Favourite.user_id == user_id
        ).delete()
        self.db.commit()

    def delete_by_article_id(self, article_id: int) -> None:
        self.db.query(Favourite).filter(Favourite.article_id == article_id).delete()
        self.db.commit()

    def delete_all_favourites_from_user(self, user_id: int) -> None:
        self.db.query(Favourite).filter(Favourite.user_id == user_id).delete()
        self.db.commit()
