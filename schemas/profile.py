"""User profile related schemas"""
from pydantic import BaseModel
from .user import NicknameRequest, PasswordRequest

class UserEditRequest(NicknameRequest):
    image_url: str | None = None

class UserEditResponse(BaseModel):
    message: str = "Profile updated successfully"

class PasswordChangeRequest(PasswordRequest):
    password: str

class PasswordChangeResponse(BaseModel):
    message: str = "Password changed successfully"

class UserProfileResponse(BaseModel):
    image_url: str
    email: str
    nickname: str