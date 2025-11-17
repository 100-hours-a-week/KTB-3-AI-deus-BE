from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from schema.db.post import PostData
from schema.db.comment import CommentPublic
from dependencies import PostDB, UserDB, CommentDB, LikeDB

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# ================ 게시글 작성 =================
class UplaodPostRequest(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    image_url: list[str] = Field(...,default_factory=[])
    poster_id: int = Field(...)

class UplaodPostResponse(BaseModel):
    message: str = Field(...)


@router.post("", status_code=200)
async def upload_post(upload_post_request: UplaodPostRequest, post_db: PostDB):
    try:
        new_post_id = post_db.add_post(
            title=upload_post_request.title,
            content=upload_post_request.content,
            poster_id=upload_post_request.poster_id,
            image_url=upload_post_request.image_url
        )
    except Exception as e:
        raise HTTPException(
            status_code=500
        )

    return UplaodPostResponse(
        message="post_success"
    )

# ================ 게시글 보기 =================
class PostResponse(BaseModel):
    message: str
    title: str
    content: str
    image_url: list[str]
    posted_date: str
    poster_image: str
    poster_nickname: str
    like: int
    view: int
    comment: list[CommentPublic]

@router.get("/{post_id}", status_code=200)
async def get_post(post_id: int, post_db: PostDB, user_db: UserDB, coomment_db: CommentDB):
    try:
        post_data = post_db.get_post_by_id(post_id)
        post_data.view += 1

        poster_data = user_db.search_user_by_id(post_data.poster_id)

        raw_comments = coomment_db.get_comments_by_post_id(post_id)

        comments = []
        for comment in raw_comments:
            comments.append(coomment_db.comment_data_2_comment_public(comment))

    except Exception as e:
        raise HTTPException(
            status_code=500
        )
    
    return PostResponse(
        message="success_get_post",
        title=post_data.title,
        content=post_data.content,
        image_url=post_data.image_url,
        posted_date=post_data.posted_date,
        poster_image=poster_data.user_profile_image_url,
        poster_nickname=poster_data.nickname,
        like=post_data.like,
        view=post_data.view,
        comment=comments
    )

# ================ 게시글 목록 ==================
class PostlistResponse(BaseModel):
    message: str = Field(...)
    data: list[PostData] = Field(...)
    next: int = Field(...)

@router.get("", status_code=200)
async def get_postlist(post_db: PostDB, offset: int = 0, limit:int = 20):

    try:
        posts, next_offset = post_db.get_posts(offset, limit)

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
        )

    return PostlistResponse(
        message="get_postlist_success",
        data=posts,
        next=next_offset
    )

# ================ 게시글 삭제 =================
class DeletePostRequest(BaseModel):
    user_id: int = Field(...)

class DeletePostResponse(BaseModel):
    message: str = Field(...)

@router.delete("/{post_id}", status_code=200)
async def delete_post(post_id: int, delete_post_request: DeletePostRequest, post_db: PostDB, user_db: UserDB):
    try:
        post = post_db.get_post_by_id(post_id)
        user = user_db.search_user_by_id(delete_post_request.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )
        
        if not post_db.delete_post_by_id(post_id):
            raise HTTPException(
                status_code=400
            )
        
    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500
        )

    return DeletePostResponse(
        message="post_delete_success"
    )


# ================ 게시글 수정 =================
class EditPostRequest(BaseModel):
    user_id: int = Field(...)
    title: str = Field(...)
    content: str = Field(...)
    image_url: list[str] = Field(...,default_factory=[])

class EditPostResponse(BaseModel):
    message: str = Field(...)


@router.patch("/{post_id}", status_code=200)
async def edit_post(post_id: int, edit_post_request: EditPostRequest, post_db: PostDB, user_db: UserDB):
    try:
        post = post_db.get_post_by_id(post_id)
        if post is None:
            raise HTTPException(
                status_code=404,
                detail="존재하지 않는 게시글 입니다."
            )
        
        user = user_db.search_user_by_id(edit_post_request.user_id)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="존재하지 않는 사용자 입니다."
            )

        if post.poster_id != user.user_id:
            raise HTTPException(
                status_code=403,
                detail="게시글 작성자가 아니라서 수정할 수 없습니다."
            )
        
        post.title = edit_post_request.title
        post.content = edit_post_request.content
        post.image_url = edit_post_request.image_url
    
    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500
        )

    return EditPostResponse(
        message="게시글을 수정하였습니다."
    )


#================= 좋아요 =====================
class LikePostRequest(BaseModel):
    user_id: int = Field(...)

class LikePostResponse(BaseModel):
    message: str = Field(...)

@router.post("/{post_id}/like", status_code=200)
async def like_post(post_id: int, like_post_requset: LikePostRequest, post_db: PostDB, user_db: UserDB, like_db: LikeDB):
    
    try:
        post = post_db.get_post_by_id(post_id)
        user = user_db.search_user_by_id(like_post_requset.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )

        if not like_db.add_like(post_id=post_id, user_id=like_post_requset.user_id):
            raise HTTPException(
                status_code=400,
                detail="이미 좋아요를 눌렀습니다."
            ) 
    
        post.like += 1
    
    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )
        
    return LikePostResponse(
        message="like_success"
    )

# ================ 좋아요 취소 =================
class UnlikePostRequest(BaseModel):
    user_id: int = Field(...)

class UnlikePostResponse(BaseModel):
    message: str = Field(...)

@router.delete("/{post_id}/like", status_code=200)
async def unlike_post(post_id: int, like_post_requset: UnlikePostRequest, post_db: PostDB, user_db: UserDB, like_db: LikeDB):
    try:
        post = post_db.get_post_by_id(post_id)
        user = user_db.search_user_by_id(like_post_requset.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )

        if not like_db.delete_like(post_id=post_id, user_id=like_post_requset.user_id):
            raise HTTPException(
                status_code=400,
                detail="좋아요를 누르지 않았습니다."
            )
        
        post.like -= 1

    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500
        )
    
    return UnlikePostResponse(
        message="unlike_success"
    )

# ================ 댓글 작성 ===================
class CommentWriteRequest(BaseModel):
    user_id: int = Field(...)
    comment: str = Field(...)

class CommentWriteResponse(BaseModel):
    comment_id: int
    message: str = Field(...)

@router.post("/{post_id}/comment", status_code=200)
async def write_comment(post_id: int, comment_write_request: CommentWriteRequest, post_db: PostDB, user_db: UserDB, comment_db: CommentDB):
    try:
        post = post_db.get_post_by_id(post_id)
        user = user_db.search_user_by_id(comment_write_request.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )
        
        time_stamp = "2001"

        comment_id = comment_db.add_comment(post_id, comment_write_request.user_id, time_stamp, comment_write_request.comment)
        
    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )
    return CommentWriteResponse(
        comment_id=comment_id,
        message="댓글을 추가하였습니다."
    )

# ================ 댓글 수정 ===================
class CommentEditRequest(BaseModel):
    comment_id: int = Field(...)
    user_id: int = Field(...)
    comment: str = Field(...)

class CommentEditResponse(BaseModel):
    message: str = Field(...)


@router.patch("/{post_id}/comment", status_code=200)
async def write_comment(post_id: int, comment_write_request: CommentEditRequest, post_db: PostDB, user_db: UserDB, comment_db: CommentDB):
    try:
        post = post_db.get_post_by_id(post_id)
        user = user_db.search_user_by_id(comment_write_request.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )
        
        comment = comment_db.get_comment_by_comment_id(comment_write_request.comment_id)

        if comment is None or comment.post_id != post_id:
            raise HTTPException(
                status_code=404,
                detail="수정할 댓글을 찾을 수 없습니다."
            )
        
        time_stamp = "2001"

        comment.comment = comment_write_request.comment
        comment.comment_date = time_stamp

    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )
    return CommentEditResponse(
        message="댓글을 수정하였습니다."
    )

# ================ 댓글 삭제 ===================
class CommentDeleteRequest(BaseModel):
    comment_id: int = Field(...)
    user_id:int = Field(...)

class CommentDeleteResponse(BaseModel):
    message: str = Field(...)

@router.delete("/{post_id}/comment", status_code=200)
async def delete_comment(post_id: int, comment_delete_request: CommentDeleteRequest, post_db:PostDB, user_db: UserDB, comment_db: CommentDB):
    try:
        post = post_db.get_post_by_id(post_id)
        user = user_db.search_user_by_id(comment_delete_request.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )
        
        if not comment_db.delete_comment_by_comment_id(comment_delete_request.comment_id):
            raise HTTPException(
                status_code=400,
                detail="댓글 삭제에 실패하였습니다."
            )
        
    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return CommentDeleteResponse(
        message="댓글을 삭제하였습니다."
    )
