from schema.db.user import UserData, UserPublic

users = [
    {"email": "test@example.com", "password": "Test1234!", "nickname": "test", "user_profile_image_url": "http" },
    {"email": "user@test.com", "password": "Valid123!", "nickname": "user", "user_profile_image_url": "http"},
    {"email": "admin@company.co.kr", "password": "Admin2024@", "nickname": "admin", "user_profile_image_url": "http"},
    {"email": "test.user+tag@example.org", "password": "MyP@ssw0rd", "nickname": "foo", "user_profile_image_url": "http"},
]

class UserDBClient:
    def __init__(self):
        self.db = []

        for user in users:
            self.add_user(**user)

    def add_user(self, email: str, password: str, nickname: str, user_profile_image_url: str) -> None:
        self.db.append(
            UserData(
                user_id=len(self.db),
                email=email,
                password=password,
                nickname=nickname,
                user_profile_image_url=user_profile_image_url
            )
        )


    def search_user_by_nickname(self, nickname: str) -> UserData | None:
        """
        닉네임으로 유저 찾기

        Args:
            nickname (str): 검색할 유저 닉네임

        Returns:
            UserData | None: 
                해당 닉네임이 있으면 UserData, 없으면 None
        """

        for user_data in self.db:
            if user_data.nickname == nickname:
                return user_data
        return None


    def search_user_by_email(self, email: str) -> UserData | None:
        """
        DB에서 email을 이용하여 사용자를 조회

        Args:
            email (str): 검색에 사용될 email

        Returns:
            UserData | None: DB에 사용자가 있으면 유저 데이터 반환
        """
        for user_data in self.db:
            if user_data.email == email:
                return user_data
        return None


    def search_user_by_id(self, user_id: int) -> UserData | None:
        """
        DB에서 user_id를 이용하여 사용자를 조회

        Args:
            user_id (int): 검색에 사용될 user_id

        Returns:
            UserData | None: DB에 사용자가 있으면 유저 데이터 반환
        """
        for user_data in self.db:
            if user_data.user_id == user_id:
                return user_data
        return None


    def user_data_2_user_public(self, data: UserData) -> UserPublic:
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


    def delete_user_by_user_id(self, user_id: int) -> bool:
        for idx, user in enumerate(self.db):
            if user.user_id == user_id:
                del self.db[idx]
                return True
        
        return False

    def authenticate_user(self, email: str, password: str) -> UserData | None:
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
        user_data = self.search_user_by_email(email)

        if user_data == None:
            return None
        # 검색해서 있으면 정보 딕션너리 반환
        if user_data.password == password:
            return user_data
        # 없으면 None을 반환
        return None