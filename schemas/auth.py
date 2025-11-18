"""Authentication related schemas"""
from pydantic import BaseModel, Field
from .user import EmailRequest, PasswordRequest, NicknameRequest

from model.user_model import UserPublic

BASE_IMAGE_URL = "http://image.base"

class SignupRequest(EmailRequest, PasswordRequest, NicknameRequest):
    image_url: str = Field(default=BASE_IMAGE_URL)

class SignupResponse(BaseModel):
    user_id: int

class LoginRequest(EmailRequest, PasswordRequest):
    pass

class LoginResponse(BaseModel):
    message: str = Field(...)
    data: UserPublic = Field(...)
