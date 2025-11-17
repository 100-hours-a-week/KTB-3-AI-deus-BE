from pydantic import BaseModel

class CommentData(BaseModel):
    comment_id: int
    post_id: int
    user_id: int
    comment_date: str
    comment: str

class CommentPublic(BaseModel):
    commenter_image: str
    commenter_nickname: str
    commented_date: str
    comment: str