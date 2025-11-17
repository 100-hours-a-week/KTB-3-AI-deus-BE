from pydantic import BaseModel, Field, field_validator

import re

EMAIL_RE = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
PW_RE = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).+$')
NICKNAME_RE = re.compile(r'^\S+$')

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

