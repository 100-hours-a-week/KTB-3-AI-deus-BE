from pydantic import BaseModel, Field
from .user_model import UserModel

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


class PostData(BaseModel):
    post_id: int = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    image_url: list[str] = Field(..., default_factory=[])
    like: int = Field(...)
    view: int = Field(...)
    poster_id: int = Field(...)
    posted_date: str = Field(...)


class PostModel():
    def __init__(self):
        
        self.post_db = []

        for post in posts:
            self.add_dummy_post(**post)

    def add_dummy_post(
            self,
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
        user_db = UserModel()
        poster_data = user_db.search_user_by_id(poster_id)
        if poster_data:
            self.post_db.append(
                PostData(
                    post_id=len(self.post_db),
                    title=title,
                    content=content,
                    image_url=image_url,
                    like=like,
                    view=view,
                    poster_id=poster_id,
                    posted_date=posted_date
                )
            )


    def add_post(
            self,
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


        self.post_db.append(
            PostData(
                post_id=len(self.post_db),
                title=title,
                content=content,
                image_url=image_url,
                like=0,
                view=0,
                poster_id=poster_id,
                posted_date="2000-10-11"
            )
        )

        return len(self.post_db) - 1


    def get_post_by_id(self, post_id: int) -> PostData | None:
        """
        DB에서 post_id를 이용하여 사용자를 조회

        Args:
            post_id (int): 검색에 사용될 post_id

        Returns:
            PostData | None: DB에 사용자가 있으면 유저 데이터 반환
        """
        for post_data in self.post_db:
            if post_data.post_id == post_id:
                return post_data
        return None


    def delete_post_by_id(self, post_id: int) -> PostData | None:
        """
        DB에서 post_id를 이용하여 사용자를 조회

        Args:
            post_id (int): 검색에 사용될 post_id

        Returns:
            PostData | None: DB에 사용자가 있으면 유저 데이터 반환
        """
        for idx, post_data in enumerate(self.post_db):
            if post_data.post_id == post_id:
                del self.post_db[idx]
                return True
        return False


    def get_posts(self, offset: int, limit: int) -> tuple[list[PostData], int]:
        next_offset = min(len(self.post_db), offset + limit)

        # DB에서 포스터를 가져오는 코드
        posts = self.post_db[offset:next_offset]

        return posts, next_offset if next_offset != len(self.post_db) else -1
