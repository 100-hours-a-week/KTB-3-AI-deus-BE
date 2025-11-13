from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
import re


EMAIL_RE = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
PW_RE = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).+$')
NICKNAME_RE = re.compile(r'^\S+$')


class UserData(BaseModel):
    email: str = Field(..., description="사용자 이메일")
    password: str = Field(..., description="사용자 비밀번호")
    nickname: str = Field(..., description="사용자 닉네임")
    user_profile_image_url: str = Field(..., description="사용자 프로필 이미지")

user = [
    {"email": "test@example.com", "password": "Test1234!", "nickname": "test"},
    {"email": "user@test.com", "password": "Valid123!", "nickname": "user"},
    {"email": "admin@company.co.kr", "password": "Admin2024@", "nickname": "admin"},
    {"email": "test.user+tag@example.org", "password": "MyP@ssw0rd", "nickname": "foo"},
]

db = []

for i in user:
    db.append(UserData(
        email=i['email'],
        password=i['password'],
        nickname=i['nickname'],
        user_profile_image_url="image_storage/" + i['nickname']
    ))

app = FastAPI()


def search_user_by_nickname(nickname: str) -> UserData | None:
    for user_data in db:
        if user_data.nickname == nickname:
            return user_data
    return None


def match_re(v: str, re: str) -> bool:
    if re.sub(r"\s+", "", v) or not re.fullmatch(v):
        return False
    
    return True


def validate_email(email: str) -> bool:
    if not match_re(email, EMAIL_RE):
        return False
    return True


def validate_password(passwd: str) -> bool:
    if not match_re(passwd, PW_RE):
        return False
    return True


def validate_nickname(nickname: str) -> bool:
    if not match_re(nickname, NICKNAME_RE):
        return False
    return True

# ================= 로그인 ==========================
class LoginRequest(BaseModel):
    email: str = Field(..., description="사용자 이메일")
    password: str = Field(..., description="사용자 비밀번호", max_length=20, min_length=8)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not validate_email(v):
            raise ValueError("Invalid email format")
        
        return v

    @field_validator('password')
    @classmethod
    def validate_passwd(cls, v: str) -> str:
        if not validate_password(v):
            raise ValueError("Invalid password format")

        return v


def search_user_by_email(email: str) -> UserData | None:
    for user_data in db:
        if user_data.email == email:
            return user_data
    return None


def authenticate_user(email: str, password: str) -> dict | None:
    # 대충 DB에서 검색 로직
    user_data = search_user_by_email(email)

    if user_data == None:
        return None
    # 검색해서 있으면 정보 딕션너리 반환
    if user_data.password == password:
        return user_data
    # 없으면 None을 반환
    return None


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


@app.post("/login")
async def login(login_request: LoginRequest):
    # 형식 검증: 솔직히 이건 프런트의 몫이다.

    user_data = authenticate_user(login_request.email, login_request.password)
    # 디비에서 이메일 검색
    if user_data is None:
        raise HTTPException(status_code=403, detail="fail login")

    return user_data


# ================ 회원 추가 ===================
class RegisterRequest(LoginRequest):
    nickname: str = Field(..., description='사용자 닉네임', max_length=10)
    profile_image: str = Field(..., description='사용자 프로필 사진')

    @field_validator('nickname')
    @classmethod
    def validate_nickname(cls, v: str) -> str:
        if not validate_nickname(v):
            raise ValueError("Invalid nickname format")

        return v

@app.patch("/register", status_code=201)
async def register_user(register_request: RegisterRequest):
    

    if search_user_by_email(register_request.email) is not None:
        raise HTTPException(
            status_code=409,
            detail="Email already in use."
        )
    
    if search_user_by_nickname(register_request.nickname) is not None:
        raise HTTPException(
            status_code=409,
            detail="nickname already in use."
        )
    
    # 저장소에 이미지 업로드
    # register_request.profile_image = 프로필 저장된 저장소 url

    user_data = UserData(**register_request)
    db.append(user_data)

    return {
        "data": user_data
    }


# ================ 회원 정보 수정 ===============
def updata_user(register_request: RegisterRequest):
    pass


@app.patch("/user/{email}/profile")
async def update_profile():
    pass
