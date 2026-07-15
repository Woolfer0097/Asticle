from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ArticleCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10000)


class ArticleUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = Field(default=None, min_length=1, max_length=10000)
    cover_url: Optional[str] = None


class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    views: int
    cover_url: Optional[str] | None
    owner_id: Optional[int] | None
