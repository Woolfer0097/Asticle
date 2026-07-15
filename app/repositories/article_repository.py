from sqlalchemy.orm import Session

from app.models.article import Article

from typing import Optional


class ArticleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, article: Article) -> Article:
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)

        return article

    def update(self, article: Article) -> Article:
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)

        return article

    def get_all(self) -> list[Article]:
        return self.db.query(Article).all()

    def get_by_id(self, article_id: int) -> Optional[Article]:
        article = self.db.query(Article).filter(Article.id == article_id).one_or_none()
        if article is not None:
            article.views += 1
            self.db.commit()
        return article

    def delete(self, article_id: int) -> None:
        self.db.query(Article).filter(Article.id == article_id).delete()
        self.db.commit()
