from fastapi import Depends
from typing import Annotated
from functools import lru_cache

from model.user_model import UserModel
from model.post_model import PostModel
from model.comment_model import CommentModel
from model.like_model import LikeModel


# 각 DB 클라이언트를 lru_cache로 Singleton처럼 사용
@lru_cache(maxsize=None)
def get_user_db() -> UserModel:
    return UserModel()


@lru_cache(maxsize=None)
def get_post_db() -> PostModel:
    return PostModel()


@lru_cache(maxsize=None)
def get_comment_db() -> CommentModel:
    return CommentModel()


@lru_cache(maxsize=None)
def get_like_db() -> LikeModel:
    return LikeModel()


# FastAPI 의존성 타입 alias
UserModelDep = Annotated[UserModel, Depends(get_user_db)]
PostModelDep = Annotated[PostModel, Depends(get_post_db)]
CommentModelDep = Annotated[CommentModel, Depends(get_comment_db)]
LikeModelDep = Annotated[LikeModel, Depends(get_like_db)]
