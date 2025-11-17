from pydantic import BaseModel

class LikeData(BaseModel):
    post_id: int
    user_id: int