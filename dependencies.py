from fastapi import Depends
from typing import Annotated
from functools import lru_cache

from DBClient.UserDBClient import UserDBClient
from DBClient.PostDBClient import PostDBClient
from DBClient.CommentDBClient import CommentDBClient
from DBClient.LikeDBClient import LikeDBClient


# 각 DB 클라이언트를 lru_cache로 Singleton처럼 사용
@lru_cache(maxsize=None)
def get_user_db() -> UserDBClient:
    return UserDBClient()


@lru_cache(maxsize=None)
def get_post_db() -> PostDBClient:
    return PostDBClient()


@lru_cache(maxsize=None)
def get_comment_db() -> CommentDBClient:
    return CommentDBClient()


@lru_cache(maxsize=None)
def get_like_db() -> LikeDBClient:
    return LikeDBClient()


# FastAPI 의존성 타입 alias
UserDB = Annotated[UserDBClient, Depends(get_user_db)]
PostDB = Annotated[PostDBClient, Depends(get_post_db)]
CommentDB = Annotated[CommentDBClient, Depends(get_comment_db)]
LikeDB = Annotated[LikeDBClient, Depends(get_like_db)]
