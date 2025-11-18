from pydantic import BaseModel, Field

class CommentPublic(BaseModel):
    commenter_image: str
    commenter_nickname: str
    commented_date: str
    comment: str

class CommentWriteRequest(BaseModel):
    user_id: int = Field(...)
    comment: str = Field(...)

class CommentWriteResponse(BaseModel):
    comment_id: int
    message: str = Field(...)

class CommentEditRequest(BaseModel):
    comment_id: int = Field(...)
    user_id: int = Field(...)
    comment: str = Field(...)

class CommentEditResponse(BaseModel):
    message: str = Field(...)

class CommentDeleteRequest(BaseModel):
    comment_id: int = Field(...)
    user_id:int = Field(...)

class CommentDeleteResponse(BaseModel):
    message: str = Field(...)

