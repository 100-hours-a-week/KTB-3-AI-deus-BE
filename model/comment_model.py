from pydantic import BaseModel
from .user_model import UserData

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


class CommentModel:
    def __init__(self):
        self.comment_db = []

    def add_dummy_comment(self, post_id: int, user_id: int, comment_date: str, comment: str) -> None:
        self.comment_db.append(
            CommentData(
                comment_id=len(self.comment_db),
                post_id=post_id,
                user_id=user_id,
                comment_date=comment_date,
                comment=comment
            )
        )
    
        # 더미 댓글 데이터 추가
        for comment in comments:
            self.add_dummy_comment(**comment)
    
    def add_comment(self, post_id: int, user_id: int, comment_date: str, comment: str) -> int:
        """
        댓글을 DB에 추가하는 함수

        포스터 id와 유저 id가 유효하면 댓글 추가

        Args:
            post_id: 댓글이 달린 포스트 ID
            user_id: 댓글 작성자 ID
            comment_data: 댓글 작성 시간
            comment: 댓글 내용
        """

        self.comment_db.append(
            CommentData(
                comment_id=len(self.comment_db),
                post_id=post_id,
                user_id=user_id,
                comment_date=comment_date,
                comment=comment
            )
        )

        return len(self.comment_db) - 1
    
    
    def get_comment_by_comment_id(self, comment_id: int) -> CommentData | None:
        for comment in self.comment_db:
            if comment.comment_id == comment_id:
                return comment
        
        return None


    def delete_comment_by_comment_id(self, comment_id: int) -> bool:
        for idx, comment in enumerate(self.comment_db):
            if comment.comment_id == comment_id:
                del self.comment_db[idx]
                return True
        
        return False


    def comment_data_2_comment_public(comment_data: CommentData, commenter:UserData) -> CommentPublic:

        return CommentPublic(
            commenter_image=commenter.user_profile_image_url,
            commenter_nickname=commenter.nickname,
            commented_date=comment_data.comment_data,
            comment=comment_data.comment
        )


    def get_comments_by_post_id(self, post_id: int) -> list[CommentData]:
        result = []

        for comment in self.comment_db:
            if comment.post_id == post_id:
                result.append(comment)
        
        return result

