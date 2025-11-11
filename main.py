from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
import re


EMAIL_RE = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
PW_RE = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).+$')

app = FastAPI()    

class LoginRequest(BaseModel):
    email: str = Field(..., description="사용자 이메일")
    password: str = Field(..., description="사용자 비밀번호", max_length=20, min_length=8)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not EMAIL_RE.fullmatch(v):
            raise ValueError("Invalid email format")

        return v

    @field_validator('password')
    @classmethod
    def validate_passwd(cls, v: str) -> str:
        if not PW_RE.fullmatch(v):
            raise ValueError("Invalid password format")

        return v



def authenticate_user(email: str, password: str) -> dict | None:
    # 대충 DB에서 검색 로직
    db = [
        {"email": "test@example.com", "password": "Test1234!", "name": "test"},
        {"email": "user@test.com", "password": "Valid123!", "name": "user"},
        {"email": "admin@company.co.kr", "password": "Admin2024@", "name": "admin"},
        {"email": "test.user+tag@example.org", "passwor": "MyP@ssw0rd", "name": "foo"},
    ]
    # 검색해서 있으면 정보 딕션너리 반환
    for user_data in db:
        if user_data['email'] == email and user_data['password'] == password:
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



