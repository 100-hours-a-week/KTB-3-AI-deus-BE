from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/users",
    tags=["Users"]
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

        if user_data:
            raise HTTPException(
                status_code=500,
                detail={
                "error": "DATABASE_ACCESS_ERROR",
                "message": "게시글 조회 중 데이터베이스 오류",
                "details": {
                    "available_posts": len(post_db),
                    "error_type": "IndexError"
                },
                "timestamp": "ㅁㅇㄹㅁㄴㄹㅇ"
            }
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

# ================ 게시글 목록 ==================
class PostlistResponse(BaseModel):
    message: str = Field(...)
    data: list[PostData] = Field(...)
    next: int = Field(...)

@app.get("/post", status_code=200)
async def get_postlist(offset: int = 0, limit:int = 20):

    try:
        next_offset = min(len(post_db), offset + limit)

        # DB에서 포스터를 가져오는 코드
        posts = post_db[offset:next_offset]
    except Exception as e:
        raise HTTPException(
            status_code=500
        )

    return PostlistResponse(
        message="get_postlist_success",
        data=posts,
        next=next_offset if next_offset != len(post_db) else -1
    )



# ================ 회원 정보 수정 ===============
class UserEditRequset(NicknameRequest):
    profile_image: str = Field(..., description='사용자 프로필 사진')

class UserEditResponse(BaseModel):
    message: str = Field(...)

@app.patch("/users/{user_id}/profile")
async def edit_profile(user_id:int, edit_user_request: UserEditRequset):
    try:
        user = search_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=404, 
                detail="사용자를 찾을 수 없습니다."
            )
        
        same_nickname_user = search_user_by_nickname(edit_user_request.nickname)

        if same_nickname_user:
            raise HTTPException(
                status_code=409,
                detail="중복되는 닉네임입니다."
            )
        
        user.nickname = edit_user_request.nickname
        user.user_profile_image_url = edit_user_request.profile_image
    
    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )

    return UserEditResponse(
        message="사용자 정보 수정이 완료되었습니다."
    )

# ================ 비밀번호 변경 ===============
class PasswordChangeRequest(PasswordRequest):
    pass

class PasswordChangeResponse(BaseModel):
    message: str = Field(...)


@app.patch("/users/{user_id}/password")
async def change_passwd(user_id: int, password_change_request: PasswordChangeRequest):
    try:
        user = search_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=404, 
                detail="사용자를 찾을 수 없습니다."
            )
        
        user.password = password_change_request.password
    
    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )

    return PasswordChangeResponse(
        message="비밀번호 수정이 완료되었습니다."
    )

# ================ 회원탈퇴 =================

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    try:
        print(db)
        user = search_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=404, 
                detail="사용자를 찾을 수 없습니다."
            )
        
        if not delete_user_by_user_id(user_id):
            raise HTTPException(
                status_code=400,
                detail="사용자를 삭제할 수 없습니다."
            )
    
    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )

    return {
        "message": "사용자 삭제를 완료하였습니다."
    }
