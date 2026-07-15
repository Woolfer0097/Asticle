from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Favourite(Base):
    __tablename__ = "favourites"

    user_id: Mapped[str] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )
    article_id: Mapped[str] = mapped_column(
        Integer, ForeignKey("articles.id"), primary_key=True
    )
