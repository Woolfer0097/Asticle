from fastapi import HTTPException, status, File
from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.user import User, UserRole
from app.repositories.article_repository import ArticleRepository
from app.repositories.favourite_repository import FavouriteRepository
from app.schemas.article import ArticleCreate, ArticleUpdate


class ArticleService:

    def __init__(self, db: Session):
        self.repository = ArticleRepository(db)
        self.favourite_repository = FavouriteRepository(db)

    def create_article(self, schema: ArticleCreate, owner: User) -> Article:
        article = Article(**schema.model_dump(), owner_id=owner.id)

        return self.repository.create(article)

    def get_articles(self) -> list[Article]:
        return self.repository.get_all()

    def get_article(self, article_id: int) -> Article:
        article = self.repository.get_by_id(article_id)

        if article is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found",
            )

        return article

    def update_article(
        self,
        article_id: int,
        schema: ArticleUpdate,
        current_user: User,
    ) -> Article:
        article = self.get_article(article_id)
        self._ensure_can_modify(article, current_user)

        if schema.title is None and schema.content is None and schema.cover_url is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        if schema.title is not None:
            article.title = schema.title

        if schema.content is not None:
            article.content = schema.content

        if schema.cover_url is not None:
            article.cover_url = schema.cover_url

        return self.repository.update(article)

    def delete_article(self, article_id: int, current_user: User) -> None:
        article = self.get_article(article_id)
        self._ensure_can_modify(article, current_user)

        self.repository.delete(article_id)
        self.favourite_repository.delete_by_article_id(article_id)

    def _ensure_can_modify(self, article: Article, current_user: User) -> None:
        if current_user.role == UserRole.ADMIN.value:
            return

        if article.owner_id == current_user.id:
            return

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can edit only your own articles",
        )
