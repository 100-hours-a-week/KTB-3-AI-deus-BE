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


def user_data_2_user_public(data:UserData) -> UserPublic:
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

# =============== 유사 디비 ========================
users = [
    {"email": "test@example.com", "password": "Test1234!", "nickname": "test", "user_profile_image_url": "http" },
    {"email": "user@test.com", "password": "Valid123!", "nickname": "user", "user_profile_image_url": "http"},
    {"email": "admin@company.co.kr", "password": "Admin2024@", "nickname": "admin", "user_profile_image_url": "http"},
    {"email": "test.user+tag@example.org", "password": "MyP@ssw0rd", "nickname": "foo", "user_profile_image_url": "http"},
]

db = []

def add_user(email, password, nickname, user_profile_image_url) -> None:
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


# 
app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    err = exc.errors()[0]
    return JSONResponse(
        status_code=422,
        content={
            "error": "요청 데이터가 올바르지 않습니다",
            "type": err['type'],
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

        if user_data is None:
            raise HTTPException(
                status_code=500,
                detail="User created but retrieval failed"
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
