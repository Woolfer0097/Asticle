from pydantic import BaseModel, ConfigDict


class FavouriteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    article_id: int
