from pydantic import BaseModel, Field

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
