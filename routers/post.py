
# ================ 게시글 작성 =================
class UplaodPostRequest(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    image_url: list[str] = Field(...,default_factory=[])
    poster_id: int = Field(...)

class UplaodPostResponse(BaseModel):
    message: str = Field(...)


@app.post("/post", status_code=200)
async def upload_post(upload_post_request: UplaodPostRequest):
    try:
        new_post_id = add_post(
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

@app.get("/post/{post_id}", status_code=200)
async def get_post(post_id: int):
    try:
        post_data = get_post_by_id(post_id)
        post_data.view += 1

        poster_data = search_user_by_id(post_data.poster_id)

        raw_comments = get_comments_by_post_id(post_id)

        comments = []
        for comment in raw_comments:
            comments.append(comment_data_2_comment_public(comment))

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

# ================ 게시글 삭제 =================
class DeletePostRequest(BaseModel):
    user_id: int = Field(...)

class DeletePostResponse(BaseModel):
    message: str = Field(...)


@app.delete("/post/{post_id}", status_code=200)
async def delete_post(post_id: int, delete_post_request: DeletePostRequest):
    try:
        post = get_post_by_id(post_id)
        user = search_user_by_id(delete_post_request.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )
        
        if not delete_post_by_id(post_id):
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


@app.patch("/post/{post_id}", status_code=200)
async def edit_post(post_id: int, edit_post_request: EditPostRequest):
    try:
        post = get_post_by_id(post_id)
        if post is None:
            raise HTTPException(
                status_code=404,
                detail="존재하지 않는 게시글 입니다."
            )
        
        user = search_user_by_id(edit_post_request.user_id)
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

@app.post("/post/{post_id}/like", status_code=200)
async def like_post(post_id: int, like_post_requset: LikePostRequest):
    
    try:
        post = get_post_by_id(post_id)
        user = search_user_by_id(like_post_requset.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )

        if not add_like(post_id=post_id, user_id=like_post_requset.user_id):
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

@app.delete("/post/{post_id}/like", status_code=200)
async def unlike_post(post_id: int, like_post_requset: UnlikePostRequest):
    try:
        post = get_post_by_id(post_id)
        user = search_user_by_id(like_post_requset.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )

        if not delete_like(post_id=post_id, user_id=like_post_requset.user_id):
            raise HTTPException(
                status_code=400
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
    message: str = Field(...)

@app.post("/post/{post_id}/comment", status_code=200)
async def write_comment(post_id: int, comment_write_request: CommentWriteRequest):
    try:
        post = get_post_by_id(post_id)
        user = search_user_by_id(comment_write_request.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )
        
        time_stamp = "2001"

        add_comment(post_id, comment_write_request.user_id, time_stamp, comment_write_request.comment)
        
    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )
    return CommentWriteResponse(
        message="댓글을 추가하였습니다."
    )

# ================ 댓글 수정 ===================
class CommentEditRequest(BaseModel):
    comment_id: int = Field(...)
    user_id: int = Field(...)
    comment: str = Field(...)

class CommentEditResponse(BaseModel):
    message: str = Field(...)


@app.patch("/post/{post_id}/comment", status_code=200)
async def write_comment(post_id: int, comment_write_request: CommentEditRequest):
    try:
        post = get_post_by_id(post_id)
        user = search_user_by_id(comment_write_request.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )
        
        comment = get_comment_by_comment_id(comment_write_request.comment_id)

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
    return CommentWriteResponse(
        message="댓글을 수정하였습니다."
    )

# ================ 댓글 삭제 ===================
class CommentDeleteRequest(BaseModel):
    comment_id: int = Field(...)
    user_id:int = Field(...)

class CommentDeleteResponse(BaseModel):
    message: str = Field(...)

@app.delete("/post/{post_id}/comment", status_code=200)
async def delete_comment(post_id: int, comment_delete_request: CommentDeleteRequest):
    try:
        post = get_post_by_id(post_id)
        user = search_user_by_id(comment_delete_request.user_id)

        if post is None or user is None:
            raise HTTPException(
                status_code=404
            )
        
        comment = get_comment_by_comment_id(comment_delete_request.comment_id)

        if comment is None or comment.post_id != post_id:
            raise HTTPException(
                status_code=404,
                detail="수정할 댓글을 찾을 수 없습니다."
            )
        
        if not delete_comment_by_comment_id(comment.comment_id):
            raise HTTPException(
                status_code=400,
                detail="댓글 삭제에 실패하였습니다."
            )
        
    except HTTPException as he:
        raise he
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=e
        )

    return CommentDeleteResponse(
        message="댓글을 삭제하였습니다."
    )
