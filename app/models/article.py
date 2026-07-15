from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(64), nullable=False)
    content: Mapped[str] = mapped_column(String)
    views: Mapped[int] = mapped_column(Integer, default=0)
    cover_url: Mapped[str] = mapped_column(String, nullable=True)
    owner_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )

    users = relationship("Favourite", backref="article")
    owner = relationship("User", backref="owned_articles")
