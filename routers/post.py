from fastapi import APIRouter, HTTPException

from dependencies import PostModelDep, UserModelDep, CommentModelDep, LikeModelDep

from schemas.post import(
    UplaodPostRequest,
    UplaodPostResponse,
    PostResponse,
    PostListResponse,
    DeletePostRequest,
    DeletePostResponse,
    EditPostRequest,
    EditPostResponse
)

from schemas.like import(
    LikePostRequest,
    LikePostResponse,
    UnlikePostRequest,
    UnlikePostResponse
)

from schemas.comment import(
    CommentEditRequest,
    CommentEditResponse,
    CommentWriteRequest,
    CommentWriteResponse,
    CommentDeleteRequest,
    CommentDeleteResponse
    
)

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# ================ 게시글 작성 =================
@router.post("", status_code=200)
async def upload_post(upload_post_request: UplaodPostRequest, post_db: PostModelDep):
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
@router.get("/{post_id}", status_code=200)
async def get_post(post_id: int, post_db: PostModelDep, user_db: UserModelDep, coomment_db: CommentModelDep):
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
@router.get("", status_code=200)
async def get_postlist(post_db: PostModelDep, offset: int = 0, limit:int = 20):

    try:
        posts, next_offset = post_db.get_posts(offset, limit)

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
        )

    return PostListResponse(
        message="get_postlist_success",
        data=posts,
        next=next_offset
    )

# ================ 게시글 삭제 =================
@router.delete("/{post_id}", status_code=200)
async def delete_post(post_id: int, delete_post_request: DeletePostRequest, post_db: PostModelDep, user_db: UserModelDep):
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
@router.patch("/{post_id}", status_code=200)
async def edit_post(post_id: int, edit_post_request: EditPostRequest, post_db: PostModelDep, user_db: UserModelDep):
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
@router.post("/{post_id}/like", status_code=200)
async def like_post(post_id: int, like_post_requset: LikePostRequest, post_db: PostModelDep, user_db: UserModelDep, like_db: LikeModelDep):
    
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
            detail=str(e)
        )
        
    return LikePostResponse(
        message="like_success"
    )

# ================ 좋아요 취소 =================
@router.delete("/{post_id}/like", status_code=200)
async def unlike_post(post_id: int, like_post_requset: UnlikePostRequest, post_db: PostModelDep, user_db: UserModelDep, like_db: LikeModelDep):
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
@router.post("/{post_id}/comment", status_code=200)
async def write_comment(post_id: int, comment_write_request: CommentWriteRequest, post_db: PostModelDep, user_db: UserModelDep, comment_db: CommentModelDep):
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
@router.patch("/{post_id}/comment", status_code=200)
async def write_comment(post_id: int, comment_write_request: CommentEditRequest, post_db: PostModelDep, user_db: UserModelDep, comment_db: CommentModelDep):
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
@router.delete("/{post_id}/comment", status_code=200)
async def delete_comment(post_id: int, comment_delete_request: CommentDeleteRequest, post_db:PostModelDep, user_db: UserModelDep, comment_db: CommentModelDep):
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
