from fastapi import APIRouter, HTTPException

from dependencies import UserModelDep

from schemas.auth import SignupRequest, SignupResponse, LoginRequest, LoginResponse 
from schemas.profile import (
    UserEditRequest, UserEditResponse, 
    PasswordChangeRequest, PasswordChangeResponse, UserProfileResponse
)

BASE_IMAGE_URL = "http://base.image.com"

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# ================= 회원가입 =========================
@router.post("/signup", status_code=201)
async def signup(signup_request: SignupRequest, user_db: UserModelDep):

    if user_db.search_user_by_email(signup_request.email) is not None:
        raise HTTPException(
            status_code=409,
            detail="Email already in use."
        )

    if user_db.search_user_by_nickname(signup_request.nickname) is not None:
        raise HTTPException(
            status_code=409,
            detail="nickname already in use."
        )

    try:
        user_data = user_db.search_user_by_email(signup_request.email)

        user_id = user_db.add_user(
            email=signup_request.email,
            password=signup_request.password,
            nickname=signup_request.nickname,
            user_profile_image_url=signup_request.image_url
        )

        if user_data is not None:
            raise HTTPException(
                status_code=500,
                detail="Failed to create user"
            )

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {e}"
        )

    return SignupResponse(
        message="signup_success",
        user_id=user_id
    )

# ================= 로그인 ==========================
@router.post("/login", status_code=200)
async def login(login_request: LoginRequest, user_db: UserModelDep):
    # 형식 검증: 솔직히 이건 프런트의 몫이다.

    user_data = user_db.authenticate_user(login_request.email, login_request.password)
    # 디비에서 이메일 검색
    if user_data is None:
        raise HTTPException(status_code=403, detail="fail login")
    
    public_user_data = user_db.user_data_2_user_public(user_data)

    return LoginResponse(
        message="login_success",
        data=public_user_data
    )

# ================= 회원 정보 조회 ====================
@router.get("/{user_id}/profile")
async def get_profile(user_id: int, user_db: UserModelDep):
    try:
        user_data = user_db.search_user_by_id(user_id)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return UserProfileResponse(
        image_url=user_data.user_profile_image_url,
        email=user_data.email,
        nickname=user_data.nickname
    )

# ================ 회원 정보 수정 =====================
@router.patch("/{user_id}/profile")
async def edit_profile(user_id:int, edit_user_request: UserEditRequest, user_db: UserModelDep):
    try:
        user = user_db.search_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=404, 
                detail="사용자를 찾을 수 없습니다."
            )
        
        same_nickname_user = user_db.search_user_by_nickname(edit_user_request.nickname)

        if same_nickname_user:
            raise HTTPException(
                status_code=409,
                detail="중복되는 닉네임입니다."
            )
        
        user.nickname = edit_user_request.nickname
        user.user_profile_image_url = edit_user_request.image_url
    
    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return UserEditResponse(
        message="사용자 정보 수정이 완료되었습니다."
    )

# ================ 비밀번호 변경 ======================
@router.patch("/{user_id}/password")
async def change_passwd(user_id: int, password_change_request: PasswordChangeRequest, user_db: UserModelDep):
    try:
        user = user_db.search_user_by_id(user_id)

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
            detail=str(e)
        )

    return PasswordChangeResponse(
        message="비밀번호 수정이 완료되었습니다."
    )

# ================ 회원탈퇴 =========================
@router.delete("/{user_id}")
async def delete_user(user_id: int, user_db: UserModelDep):
    try:
        user = user_db.search_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=404, 
                detail="사용자를 찾을 수 없습니다."
            )
        
        if not user_db.delete_user_by_user_id(user_id):
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
