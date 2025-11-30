from pydantic import BaseModel, Field

from model.comment_model import CommentPublic
from model.post_model import PostData

class UplaodPostRequest(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    image_url: list[str] = Field(...,default_factory=[])
    poster_id: int = Field(...)

class UplaodPostResponse(BaseModel):
    new_post_id: int
    message: str = Field(...)

class PostResponse(BaseModel):
    message: str
    title: str
    content: str
    image_url: list[str]
    posted_date: str
    poster_image: str
    poster_nickname: str
    like: int
    view: int
    comment: list[CommentPublic]

class PostListResponse(BaseModel):
    message: str = Field(...)
    data: list[PostData] = Field(...)
    next: int = Field(...)


class DeletePostRequest(BaseModel):
    user_id: int = Field(...)

class DeletePostResponse(BaseModel):
    message: str = Field(...)

class EditPostRequest(BaseModel):
    user_id: int = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    image_url: list[str] = Field(...,default_factory=[])

class EditPostResponse(BaseModel):
    message: str = Field(...)




