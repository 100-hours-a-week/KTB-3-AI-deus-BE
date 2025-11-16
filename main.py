from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
import re


EMAIL_RE = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
PW_RE = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).+$')
NICKNAME_RE = re.compile(r'^\S+$')
BASE_IMAGE_URL = "http"

# =============== 구조체 ========================
class EmailRequest(BaseModel):
    email: str = Field(..., description="사용자 이메일")

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not validate_email(v):
            raise ValueError("Invalid email format")
        
        return v

class PasswordRequest(BaseModel):
    password: str = Field(..., description="사용자 비밀번호", max_length=20, min_length=8)

    @field_validator('password')
    @classmethod
    def validate_passwd(cls, v: str) -> str:
        if not validate_password(v):
            raise ValueError("Invalid password format")

        return v

class NicknameRequest(BaseModel):
    nickname: str = Field(..., description='사용자 닉네임', max_length=10)

    @field_validator('nickname')
    @classmethod
    def validate_nickname(cls, v: str) -> str:
        if not validate_nickname(v):
            raise ValueError("Invalid nickname format")

        return v

class UserPublic(BaseModel):
    user_id: int = Field(...)
    email: str = Field(...)
    nickname: str = Field(...)
    user_profile_image_url: str = Field(...)

class UserData(BaseModel):
    """
    DB에 저장되는 사용자 정보
    """
    user_id: int = Field(...)
    email: str = Field(..., description="사용자 이메일")
    password: str = Field(..., description="사용자 비밀번호")
    nickname: str = Field(..., description="사용자 닉네임")
    user_profile_image_url: str = Field(..., description="사용자 프로필 이미지")

class PostData(BaseModel):
    post_id: int = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    image_url: list[str] = Field(..., default_factory=[])
    like: int = Field(...)
    view: int = Field(...)
    poster_id: int = Field(...)
    posted_date: str = Field(...)

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

class LikeData(BaseModel):
    post_id: int
    user_id: int
    
# =============== 유틸 함수 ========================
def search_user_by_nickname(nickname: str) -> UserData | None:
    """
    닉네임으로 유저 찾기

    Args:
        nickname (str): 검색할 유저 닉네임

    Returns:
        UserData | None: 
            해당 닉네임이 있으면 UserData, 없으면 None
    """

    for user_data in db:
        if user_data.nickname == nickname:
            return user_data
    return None


def search_user_by_email(email: str) -> UserData | None:
    """
    DB에서 email을 이용하여 사용자를 조회

    Args:
        email (str): 검색에 사용될 email

    Returns:
        UserData | None: DB에 사용자가 있으면 유저 데이터 반환
    """
    for user_data in db:
        if user_data.email == email:
            return user_data
    return None


def search_user_by_id(user_id: int) -> UserData | None:
    """
    DB에서 user_id를 이용하여 사용자를 조회

    Args:
        user_id (int): 검색에 사용될 user_id

    Returns:
        UserData | None: DB에 사용자가 있으면 유저 데이터 반환
    """
    for user_data in db:
        if user_data.user_id == user_id:
            return user_data
    return None


def authenticate_user(email: str, password: str) -> UserData | None:
    """
    DB에서 사용자를 검색하고 인증을 수행하는 함수

    이메일과 비밀번호를 검증하여 사용자 인증을 처리한다
    DB에서 이메일로 사용자를 검색한 후,
    비밀번호를 이용하여 검증한다

    Args:
        email (str): 인증을 원하는 사용자 이메일 주소
        password (str): 검증할 비밀번호

    Returns:
        UserData | None: 인증 성공시 사용자 정보를 반환
                        인증 실패시 None 반환
    
    """
    # 대충 DB에서 검색 로직
    user_data = search_user_by_email(email)

    if user_data == None:
        return None
    # 검색해서 있으면 정보 딕션너리 반환
    if user_data.password == password:
        return user_data
    # 없으면 None을 반환
    return None


def match_re(v: str, ex: str) -> bool:
    """
    공백의 유무를 확인하고 정규 표현식과 비교

    Args:
        v (str): 비교할 문자열
        ex (str): 비교할 정규표현식

    Returns:
        bool: _description_
    """
    if bool(re.search(r"\s", v)) or not ex.fullmatch(v):
        return False
    
    return True


def validate_email(email: str) -> bool:
    """
    이메일이 규칙에 맞는 맞는지 확인

    Args:
        email (str): 확인할 이미지

    Returns:
        bool: _description_
    """
    if not match_re(email, EMAIL_RE):
        return False
    return True


def validate_password(passwd: str) -> bool:
    """
    패스워드가 규칙에 맞는지 확인

    Args:
        passwd (str): 확인할 패스워드

    Returns:
        bool: _description_
    """
    if not match_re(passwd, PW_RE):
        return False
    return True


def validate_nickname(nickname: str) -> bool:
    """
    닉네임 규칙에 맞는지 확인

    Args:
        nickname (str): 확인할 문자열

    Returns:
        bool: _description_
    """
    if not match_re(nickname, NICKNAME_RE):
        return False
    return True


def user_data_2_user_public(data: UserData) -> UserPublic:
    """
    DB에서 가져온 데이터를 민감한 정보를 제외한 외부로 전송한 가는 데이터로 변경

    Args:
        data (UserData): 변경할 데이터

    Returns:
        UserPublic: 외부로 전송가능한 모든 유저 정보
    """
    return UserPublic(
        user_id=data.user_id,
        email=data.email,
        nickname=data.nickname,
        user_profile_image_url=data.user_profile_image_url
    )


def get_post_by_id(post_id: int) -> PostData | None:
    """
    DB에서 post_id를 이용하여 사용자를 조회

    Args:
        post_id (int): 검색에 사용될 post_id

    Returns:
        PostData | None: DB에 사용자가 있으면 유저 데이터 반환
    """
    for post_data in post_db:
        if post_data.post_id == post_id:
            return post_data
    return None


def get_comments_by_post_id(post_id: int) -> list[CommentData]:
    result = []

    for comment in comment_db:
        if comment.post_id == post_id:
            result.append(comment)
    
    return result


def comment_data_2_comment_public(comment_data: CommentData) -> CommentPublic:
    commenter = search_user_by_id(comment_data.user_id)

    return CommentPublic(
        commenter_image=commenter.user_profile_image_url,
        commenter_nickname=commenter.nickname,
        commented_date=comment_data.comment_data,
        comment=comment_data.comment
    )


def delete_post_by_id(post_id: int) -> PostData | None:
    """
    DB에서 post_id를 이용하여 사용자를 조회

    Args:
        post_id (int): 검색에 사용될 post_id

    Returns:
        PostData | None: DB에 사용자가 있으면 유저 데이터 반환
    """
    for idx, post_data in enumerate(post_db):
        if post_data.post_id == post_id:
            del post_db[idx]
            return True
    return False

def delete_like(post_id: int, user_id: int) -> bool:
    for idx, like in enumerate(like_db):
        if like.post_id == post_id and like.user_id == user_id:
            del like_db[idx]
            return True
    
    return False


# =============== 유사 디비 ========================
users = [
    {"email": "test@example.com", "password": "Test1234!", "nickname": "test", "user_profile_image_url": "http" },
    {"email": "user@test.com", "password": "Valid123!", "nickname": "user", "user_profile_image_url": "http"},
    {"email": "admin@company.co.kr", "password": "Admin2024@", "nickname": "admin", "user_profile_image_url": "http"},
    {"email": "test.user+tag@example.org", "password": "MyP@ssw0rd", "nickname": "foo", "user_profile_image_url": "http"},
]

db = []

def add_user(email: str, password: str, nickname: str, user_profile_image_url: str) -> None:
    db.append(
        UserData(
            user_id=len(db),
            email=email,
            password=password,
            nickname=nickname,
            user_profile_image_url=user_profile_image_url
        )
    )


for user in users:
    add_user(**user)

# 10개의 포스트 더미 데이터
posts = [
    {
        "title": "FastAPI 시작하기: 첫 번째 프로젝트",
        "content": "FastAPI는 현대적이고 빠른 웹 프레임워크입니다. Python 3.7+를 사용하여 API를 구축하기 위한 표준 Python 타입 힌트를 기반으로 합니다. 이 글에서는 FastAPI를 시작하는 방법을 알아봅니다.",
        "poster_id": 0,  # test user
        "image_url": ["https://example.com/images/fastapi1.jpg", "https://example.com/images/fastapi2.jpg"],
        "like": 15,
        "view": 234,
        "posted_date": "2024-01-15T10:30:00"
    },
    {
        "title": "Python 타입 힌트 완벽 가이드",
        "content": "Python 3.5부터 도입된 타입 힌트는 코드의 가독성과 유지보수성을 크게 향상시킵니다. 이 글에서는 기본적인 타입 힌트부터 고급 기능까지 다룹니다.",
        "poster_id": 1,  # user
        "image_url": ["https://example.com/images/python_types.png"],
        "like": 42,
        "view": 567,
        "posted_date": "2024-01-20T14:45:00"
    },
    {
        "title": "RESTful API 설계 베스트 프랙티스",
        "content": "REST는 Representational State Transfer의 약자로, 웹 서비스를 위한 아키텍처 스타일입니다. 효과적인 RESTful API 설계를 위한 핵심 원칙과 실용적인 팁을 공유합니다.",
        "poster_id": 2,  # admin
        "image_url": [],
        "like": 89,
        "view": 1203,
        "posted_date": "2024-02-01T09:00:00"
    },
    {
        "title": "Pydantic으로 데이터 검증 마스터하기",
        "content": "Pydantic은 Python의 데이터 검증 라이브러리로, FastAPI의 핵심 구성 요소입니다. 이 튜토리얼에서는 Pydantic의 강력한 기능들을 살펴봅니다.",
        "poster_id": 3,  # foo
        "image_url": ["https://example.com/images/pydantic_logo.svg", "https://example.com/images/validation.jpg"],
        "like": 27,
        "view": 456,
        "posted_date": "2024-02-10T16:20:00"
    },
    {
        "title": "비동기 프로그래밍: async와 await 이해하기",
        "content": "Python의 비동기 프로그래밍은 I/O 바운드 작업의 성능을 크게 향상시킬 수 있습니다. async와 await 키워드를 사용하여 효율적인 비동기 코드를 작성하는 방법을 알아봅시다.",
        "poster_id": 0,  # test user
        "image_url": ["https://example.com/images/async_python.png"],
        "like": 63,
        "view": 892,
        "posted_date": "2024-02-15T11:30:00"
    },
    {
        "title": "Docker로 FastAPI 애플리케이션 배포하기",
        "content": "컨테이너화는 현대 애플리케이션 배포의 표준이 되었습니다. Docker를 사용하여 FastAPI 애플리케이션을 컨테이너화하고 배포하는 완벽한 가이드입니다.",
        "poster_id": 2,  # admin
        "image_url": ["https://example.com/images/docker_fastapi.jpg", "https://example.com/images/container.png", "https://example.com/images/deployment.jpg"],
        "like": 105,
        "view": 1567,
        "posted_date": "2024-02-20T13:45:00"
    },
    {
        "title": "JWT 인증 구현하기: 보안 최우선",
        "content": "JSON Web Token(JWT)은 웹 애플리케이션에서 안전한 인증을 구현하는 표준 방법입니다. FastAPI와 JWT를 사용한 인증 시스템 구축 방법을 단계별로 설명합니다.",
        "poster_id": 1,  # user
        "image_url": ["https://example.com/images/jwt_flow.png"],
        "like": 78,
        "view": 1089,
        "posted_date": "2024-03-01T10:00:00"
    },
    {
        "title": "데이터베이스 연동: SQLAlchemy와 함께",
        "content": "SQLAlchemy는 Python의 강력한 ORM 라이브러리입니다. FastAPI와 SQLAlchemy를 연동하여 효율적인 데이터베이스 작업을 수행하는 방법을 배워봅시다.",
        "poster_id": 3,  # foo
        "image_url": ["https://example.com/images/sqlalchemy.jpg", "https://example.com/images/database_schema.png"],
        "like": 51,
        "view": 723,
        "posted_date": "2024-03-05T15:30:00"
    },
    {
        "title": "테스트 자동화: pytest로 API 테스트하기",
        "content": "테스트는 안정적인 소프트웨어 개발의 핵심입니다. pytest와 FastAPI의 TestClient를 사용하여 API 엔드포인트를 효과적으로 테스트하는 방법을 알아봅니다.",
        "poster_id": 0,  # test user
        "image_url": [],
        "like": 34,
        "view": 445,
        "posted_date": "2024-03-10T17:15:00"
    },
    {
        "title": "성능 최적화 팁: FastAPI를 더 빠르게",
        "content": "FastAPI는 이미 빠르지만, 추가적인 최적화로 더 나은 성능을 얻을 수 있습니다. 캐싱, 연결 풀링, 비동기 처리 등 다양한 최적화 기법을 소개합니다.",
        "poster_id": 2,  # admin
        "image_url": ["https://example.com/images/performance.jpg", "https://example.com/images/optimization.png"],
        "like": 92,
        "view": 1456,
        "posted_date": "2024-03-15T12:00:00"
    }
]

post_db = []

def add_dummy_post(
    title: str,
    content: str,
    poster_id: int,
    image_url: list[str],
    like: int,
    view: int,
    posted_date: str
) -> None:
    """
    포스터를 DB에 추가해주는 함수

    Args:
        title (str): 포스터의 제목
        content (str): 포스터의 내용
        poster_id (int): 작성자
        image_url (list[str]): 포스터의 이미지
        like (int): 포스터의 좋아요수
        view (int): 
        posted_date (str): _description_
    """
    poster_data = search_user_by_id(poster_id)

    if poster_data:
        post_db.append(
            PostData(
                post_id=len(post_db),
                title=title,
                content=content,
                image_url=image_url,
                like=like,
                view=view,
                poster_id=poster_id,
                posted_date=posted_date
            )
        )

# 더미 포스트 데이터 추가
for post in posts:
    add_dummy_post(**post)


def add_post(
    title: str,
    content: str,
    poster_id: int,
    image_url: list[str] = [],
) -> int:
    """
    포스터를 DB에 추가해주는 함수

    Args:
        title (str): 포스터의 제목
        content (str): 포스터의 내용
        poster_id (int): 작성자
        image_url (list[str]): 포스터의 이미지
    
    Return:
        int: 추가된 포스터의 id값
    """
    poster_data = search_user_by_id(poster_id)

    if poster_data:
        post_db.append(
            PostData(
                post_id=len(post_db),
                title=title,
                content=content,
                image_url=image_url,
                like=0,
                view=0,
                poster_id=poster_id,
                posted_date="2000-10-11"
            )
        )

    return len(post_db) - 1

# 10개의 댓글 더미 데이터
comments = [
    {
        "post_id": 0,  # "FastAPI 시작하기" 포스트
        "user_id": 1,  # user
        "comment_date": "2024-01-16T09:15:00",
        "comment": "FastAPI 정말 빠르고 좋네요! 이 글 덕분에 쉽게 시작할 수 있었습니다."
    },
    {
        "post_id": 1,  # "Python 타입 힌트" 포스트
        "user_id": 2,  # admin
        "comment_date": "2024-01-21T11:30:00",
        "comment": "타입 힌트는 처음에 번거로워 보였는데, 익숙해지니 디버깅이 훨씬 편해졌어요."
    },
    {
        "post_id": 2,  # "RESTful API 설계" 포스트
        "user_id": 3,  # foo
        "comment_date": "2024-02-02T14:20:00",
        "comment": "REST API 설계 원칙 정리가 깔끔하네요. 북마크 해둡니다!"
    },
    {
        "post_id": 3,  # "Pydantic 데이터 검증" 포스트
        "user_id": 0,  # test
        "comment_date": "2024-02-11T10:45:00",
        "comment": "Pydantic의 자동 검증 기능이 정말 강력합니다. 실무에서 많은 도움이 되고 있어요."
    },
    {
        "post_id": 4,  # "비동기 프로그래밍" 포스트
        "user_id": 1,  # user
        "comment_date": "2024-02-16T15:00:00",
        "comment": "async/await 패턴 설명이 명확해서 이해하기 쉬웠습니다. 감사합니다!"
    },
    {
        "post_id": 5,  # "Docker로 FastAPI" 포스트
        "user_id": 3,  # foo
        "comment_date": "2024-02-21T09:30:00",
        "comment": "Docker 컨테이너화 가이드 따라하니 바로 배포 성공했습니다. 최고예요!"
    },
    {
        "post_id": 6,  # "JWT 인증 구현" 포스트
        "user_id": 0,  # test
        "comment_date": "2024-03-02T16:45:00",
        "comment": "JWT 인증 구현 예제 코드가 실용적이네요. 바로 적용해봐야겠습니다."
    },
    {
        "post_id": 7,  # "SQLAlchemy 연동" 포스트
        "user_id": 2,  # admin
        "comment_date": "2024-03-06T12:00:00",
        "comment": "SQLAlchemy ORM 설명이 상세해서 좋았습니다. 다음 포스트도 기대됩니다!"
    },
    {
        "post_id": 0,  # "FastAPI 시작하기" 포스트 (두 번째 댓글)
        "user_id": 3,  # foo
        "comment_date": "2024-01-17T14:30:00",
        "comment": "저도 이 글 보고 FastAPI 입문했는데 정말 도움이 많이 됐습니다!"
    },
    {
        "post_id": 9,  # "성능 최적화 팁" 포스트
        "user_id": 1,  # user
        "comment_date": "2024-03-16T10:15:00",
        "comment": "성능 최적화 팁들이 정말 유용합니다. 특히 캐싱 부분이 도움이 많이 됐어요."
    }
]

comment_db = []

def add_dummy_comment(post_id: int, user_id: int, comment_date: str, comment: str) -> None:
    if post_id < len(post_db):
        user_data = search_user_by_id(user_id)
        if user_data:
            comment_db.append(
                CommentData(
                    comment_id=len(comment_db),
                    post_id=post_id,
                    user_id=user_id,
                    comment_date=comment_date,
                    comment=comment
                )
            )

# 더미 댓글 데이터 추가
for comment in comments:
    add_dummy_comment(**comment)

# 10개의 좋아요 더미 데이터
likes = [
    {
        "post_id": 0,  # "FastAPI 시작하기" 포스트
        "user_id": 1   # user가 좋아요
    },
    {
        "post_id": 0,  # "FastAPI 시작하기" 포스트
        "user_id": 2   # admin도 좋아요
    },
    {
        "post_id": 1,  # "Python 타입 힌트" 포스트
        "user_id": 0   # test가 좋아요
    },
    {
        "post_id": 2,  # "RESTful API 설계" 포스트
        "user_id": 3   # foo가 좋아요
    },
    {
        "post_id": 5,  # "Docker로 FastAPI" 포스트
        "user_id": 0   # test가 좋아요
    },
    {
        "post_id": 5,  # "Docker로 FastAPI" 포스트
        "user_id": 1   # user도 좋아요
    },
    {
        "post_id": 6,  # "JWT 인증 구현" 포스트
        "user_id": 2   # admin이 좋아요
    },
    {
        "post_id": 9,  # "성능 최적화 팁" 포스트
        "user_id": 1   # user가 좋아요
    },
    {
        "post_id": 9,  # "성능 최적화 팁" 포스트
        "user_id": 3   # foo도 좋아요
    },
    {
        "post_id": 3,  # "Pydantic 데이터 검증" 포스트
        "user_id": 0   # test가 좋아요
    }
]

like_db = []

def add_dummy_like(post_id: int, user_id: int) -> bool:
    """
    좋아요를 DB에 추가하는 함수

    중복 좋아요는 방지합니다.

    Args:
        post_id: 좋아요를 누를 포스트 ID
        user_id: 좋아요를 누르는 사용자 ID

    Returns:
        bool: 좋아요 추가 성공 여부
    """
    # 이미 좋아요를 눌렀는지 확인
    for like in like_db:
        if like.post_id == post_id and like.user_id == user_id:
            return False  # 이미 좋아요를 누름

    # 유효한 포스트와 사용자인지 확인
    if post_id < len(post_db) and user_id < len(db):
        like_db.append(
            LikeData(
                post_id=post_id,
                user_id=user_id
            )
        )
        return True
    return False

# 더미 좋아요 데이터 추가
for like in likes:
    add_dummy_like(**like)

# like_db 데이터에 따라 각 포스트의 좋아요 수 업데이트
def update_post_like_counts():
    """
    like_db의 데이터를 기반으로 각 포스트의 좋아요 수를 업데이트
    """
    # 모든 포스트의 좋아요 수를 0으로 초기화
    for post in post_db:
        post.like = 0

    # like_db를 순회하며 각 포스트의 좋아요 수 계산
    for like in like_db:
        if like.post_id < len(post_db):
            post_db[like.post_id].like += 1

# 포스트의 좋아요 수 업데이트
update_post_like_counts()

def add_like(post_id: int, user_id: int) -> bool:
    for liked in like_db:
        if liked.post_id == post_id and liked.user_id == user_id:
            return False

    like_db.append(
        LikeData(
            post_id=post_id,  # 키워드 인자로 수정
            user_id=user_id   # 키워드 인자로 수정
        )
    )

    return True

def add_comment(post_id: int, user_id: int, comment_date: str, comment: str) -> None:
    """
    댓글을 DB에 추가하는 함수

    포스터 id와 유저 id가 유효하면 댓글 추가

    Args:
        post_id: 댓글이 달린 포스트 ID
        user_id: 댓글 작성자 ID
        comment_data: 댓글 작성 시간
        comment: 댓글 내용
    """

    if post_id < len(post_db) and user_id < len(db):
        comment_db.append(
            CommentData(
                comment_id=len(comment_db),
                post_id=post_id,
                user_id=user_id,
                comment_date=comment_date,
                comment=comment
            )
        )

# ================ 앱 ==================================
app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    err = exc.errors()[0]
    return JSONResponse(
        status_code=422,
        content={
            "error": "요청 데이터가 올바르지 않습니다",
            "type": err['type'],
            "loc": err['loc'],
            "details": err['msg']
        }
    )

# ================= 회원가입 =========================
class SignupRequest(EmailRequest, PasswordRequest, NicknameRequest):
    image_url: str = Field(default=BASE_IMAGE_URL)

class SignupData(BaseModel):
    user_id: int = Field(...)

class SignupResponse(BaseModel):
    message: str = Field(...)
    data: SignupData = Field(...)


@app.post("/users/signup", status_code=201)
async def signup(signup_request: SignupRequest):

    if search_user_by_email(signup_request.email) is not None:
        raise HTTPException(
            status_code=409,
            detail="Email already in use."
        )
    
    if search_user_by_nickname(signup_request.nickname) is not None:
        raise HTTPException(
            status_code=409,
            detail="nickname already in use."
        )
    
    # 저장소에 이미지 업로드
    # signup_request.image_url = 프로필 저장된 저장소 url

    try:
        add_user(
            email=signup_request.email,
            password=signup_request.password,
            nickname=signup_request.nickname,
            user_profile_image_url=signup_request.image_url
        )

        user_data = search_user_by_email(signup_request.email)

        if user_data:
            raise HTTPException(
                status_code=500,
                detail={
                "error": "DATABASE_ACCESS_ERROR",
                "message": "게시글 조회 중 데이터베이스 오류",
                "details": {
                    "available_posts": len(post_db),
                    "error_type": "IndexError"
                },
                "timestamp": "ㅁㅇㄹㅁㄴㄹㅇ"
            }
            )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {e}"
        )

    return SignupResponse(
        message="signup_success",
        data=SignupData(
            user_id=user_data.user_id
        )
    )

# ================= 로그인 ==========================
class LoginRequest(EmailRequest, PasswordRequest):
    pass

class LoginResponse(BaseModel):
    message: str = Field(...)
    data: UserPublic = Field(...)

@app.post("/users/login", status_code=200)
async def login(login_request: LoginRequest):
    # 형식 검증: 솔직히 이건 프런트의 몫이다.

    user_data = authenticate_user(login_request.email, login_request.password)
    # 디비에서 이메일 검색
    if user_data is None:
        raise HTTPException(status_code=403, detail="fail login")
    
    public_user_data = user_data_2_user_public(user_data)

    return LoginResponse(
        message="login_success",
        data=public_user_data
    )

# ================ 게시글 목록 ==================
class PostlistResponse(BaseModel):
    message: str = Field(...)
    data: list[PostData] = Field(...)
    next: int = Field(...)

@app.get("/post", status_code=200)
async def get_postlist(offset: int = 0, limit:int = 20):

    try:
        next_offset = min(len(post_db), offset + limit)

        # DB에서 포스터를 가져오는 코드
        posts = post_db[offset:next_offset]
    except Exception as e:
        raise HTTPException(
            status_code=500
        )

    return PostlistResponse(
        message="get_postlist_success",
        data=posts,
        next=next_offset if next_offset != len(post_db) else -1
    )

# ================ 게시글 작성 =================
class UplaodPostRequest(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    image_url: list[str] = Field(...,default_factory=[])
    poster_id: int = Field(...)

class UplaodPostResponse(BaseModel):
    message: str = Field(...)


@app.post("/post", status_code=200)
async def upload_post(upload_post_request: UplaodPostRequest):
    try:
        new_post_id = add_post(
            title=upload_post_request.title,
            content=upload_post_request.content,
            poster_id=upload_post_request.poster_id,
            image_url=upload_post_request.image_url
        )
    except Exception as e:
        raise HTTPException(
            status_code=500
        )

    return UplaodPostResponse(
        message="post_success"
    )

# ================ 게시글 보기 =================
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

@app.get("/post/{post_id}", status_code=200)
async def get_post(post_id: int):
    try:
        post_data = get_post_by_id(post_id)
        post_data.view += 1

        poster_data = search_user_by_id(post_data.poster_id)

        raw_comments = get_comments_by_post_id(post_id)

        comments = []
        for comment in raw_comments:
            comments.append(comment_data_2_comment_public(comment))

    except Exception as e:
        raise HTTPException(
            status_code=500
        )
    
    return PostResponse(
        message="success_get_post",
        title=post_data.title,
        content=post_data.content,
        image_url=post_data.image_url,
        posted_date=post_data.posted_date,
        poster_image=poster_data.user_profile_image_url,
        poster_nickname=poster_data.nickname,
        like=post_data.like,
        view=post_data.view,
        comment=comments
    )

# ================ 게시글 작성 =================
class DeletePostResponse(BaseModel):
    message: str = Field(...)


@app.delete("/post/{post_id}", status_code=200)
async def delete_post(post_id: int):
    try:
        if not delete_post_by_id(post_id):
            HTTPException(
                status_code=400
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=500
        )

    return DeletePostResponse(
        message="post_delete_success"
    )

#================= 좋아요 =====================
class LikePostRequest(BaseModel):
    user_id: int = Field(...)

class LikePostResponse(BaseModel):
    message: str = Field(...)

@app.post("/post/{post_id}/like", status_code=200)
async def like_post(post_id: int, like_post_requset: LikePostRequest):
    
    try:
        post = get_post_by_id(post_id)
        user = search_user_by_id(like_post_requset.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )

        if not add_like(post_id=post_id, user_id=like_post_requset.user_id):
            raise HTTPException(
                status_code=400,
                detail="이미 좋아요를 눌렀습니다."
            ) 
    
        post.like += 1
    
    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )
        
    return LikePostResponse(
        message="like_success"
    )

# ================ 좋아요 취소 =================
class UnlikePostRequest(BaseModel):
    user_id: int = Field(...)

class UnlikePostResponse(BaseModel):
    message: str = Field(...)

@app.delete("/post/{post_id}/like", status_code=200)
async def unlike_post(post_id: int, like_post_requset: UnlikePostRequest):
    try:
        post = get_post_by_id(post_id)
        user = search_user_by_id(like_post_requset.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )

        if not delete_like(post_id=post_id, user_id=like_post_requset.user_id):
            raise HTTPException(
                status_code=400
            )
        
        post.like -= 1

    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500
        )
    
    return UnlikePostResponse(
        message="unlike_success"
    )

# ================ 댓글 작성 ===================
class CommentWriteRequest(BaseModel):
    user_id: int = Field(...)
    comment: str = Field(...)

class CommentWriteResponse(BaseModel):
    message: str = Field(...)

@app.post("/post/{post_id}/comment", status_code=200)
async def write_comment(post_id: int, comment_write_request: CommentWriteRequest):
    try:
        post = get_post_by_id(post_id)
        user = search_user_by_id(comment_write_request.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )
        
        time_stamp = "2001"

        add_comment(post_id, comment_write_request.user_id, time_stamp, comment_write_request.comment)
        
    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )
    return CommentWriteResponse(
        message="댓글을 추가하였습니다."
    )

# ================ 회원 정보 수정 ===============
class ChangeUserDate(LoginRequest):
    nickname: str = Field(..., description='사용자 닉네임', max_length=10)
    profile_image: str = Field(..., description='사용자 프로필 사진')

    @field_validator('nickname')
    @classmethod
    def validate_nickname(cls, v: str) -> str:
        if not validate_nickname(v):
            raise ValueError("Invalid nickname format")

        return v


@app.patch("/user/{email}/data")
async def update_profile(change_user_data: ChangeUserDate):
    
    user_data = search_user_by_email(change_user_data.email)

    if user_data is None:
        raise HTTPException(status_code=403, detail="fail to find user")
    
    user_data.nickname = change_user_data.nickname
    user_data.user_profile_image_url = change_user_data.profile_image

    return {
        "data": user_data
    }

@app.patch("/user/{email}/password")
async def update_password(change_user_data: LoginRequest):
    
    user_data = search_user_by_email(change_user_data.email)

    if user_data is None:
        raise HTTPException(status_code=403, detail="fail to find user")
    
    user_data.password = change_user_data.password

    return {
        "data": user_data
    }
