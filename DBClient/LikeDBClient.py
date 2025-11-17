from schema.db.like import LikeData

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


class LikeDBClient:
    def __init__(self):

        # 10개의 좋아요 더미 데이터
        
        self.like_db = []

        # 더미 좋아요 데이터 추가
        for like in likes:
            self.add_dummy_like(**like)


    def add_dummy_like(self, post_id: int, user_id: int) -> bool:
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
        for like in self.like_db:
            if like.post_id == post_id and like.user_id == user_id:
                return False  # 이미 좋아요를 누름

        # 유효한 포스트와 사용자인지 확인
        self.like_db.append(
            LikeData(
                post_id=post_id,
                user_id=user_id
            )
        )
        return True

    def add_like(self, post_id: int, user_id: int) -> bool:
        for liked in self.like_db:
            if liked.post_id == post_id and liked.user_id == user_id:
                return False

        self.like_db.append(
            LikeData(
                post_id=post_id,  # 키워드 인자로 수정
                user_id=user_id   # 키워드 인자로 수정
            )
        )

        return True
    

    def delete_like(self, post_id: int, user_id: int) -> bool:
        for idx, like in enumerate(self.like_db):
            if like.post_id == post_id and like.user_id == user_id:
                del self.like_db[idx]
                return True
        
        return False

