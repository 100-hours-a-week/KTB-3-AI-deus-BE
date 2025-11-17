from pydantic import BaseModel, Field

class PostData(BaseModel):
    post_id: int = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    image_url: list[str] = Field(..., default_factory=[])
    like: int = Field(...)
    view: int = Field(...)
    poster_id: int = Field(...)
    posted_date: str = Field(...)

