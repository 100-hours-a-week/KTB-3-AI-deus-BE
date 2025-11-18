from pydantic import BaseModel, Field

class LikePostRequest(BaseModel):
    user_id: int = Field(...)

class LikePostResponse(BaseModel):
    message: str = Field(...)

class UnlikePostRequest(BaseModel):
    user_id: int = Field(...)

class UnlikePostResponse(BaseModel):
    message: str = Field(...)