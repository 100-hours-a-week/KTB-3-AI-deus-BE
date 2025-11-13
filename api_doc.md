


{
    "message": "login_success",
    "data": {
        "user_id": 1,
        "nickname": test,
        "profile_image": str
    }
}


# login
{
    "email": "test@test.com",
    "password": "test1234",
}
# 200
'''
"{
    ""message"": ""login_success"",
    ""data"": {
        ""user_id"": 1,
        ""nickname"": test
        ""profile_image"": str
    }
}"
400	"{
    ""message"": ""bad_request"",
    ""data"": null
}"
401	"{
    ""message"": ""login_fail"",
    ""data"": null
}"
403	"{
    ""message"": ""account_blocked"",
    ""data"": null
}"
422	"{
    ""message"": ""invalid format"",
    ""data"": null
}"
500	"{
    ""message"" : ""internal_server_error"",
    ""data"" : null
}"
'''
# 게시글 목록

# 200
{
    "message": "login_success",
    "data": [
        {
            "id": 1,
            "like": 1,
            "comment": 1,
            "view": 1,
            "poster": 12,
            "poster_image": hh
            "posted_date": 2001
        },
    ],
    "next": false
}

# 400
{
    "message": "bad_request",
    "data": null,
    "next": True
}
# 게시글 보기
{

}

# 200
{
    "message": "bad_request",
    "title": "제목",
    "content": "내용",
    "image_url": "이미지 링크",
    "poster_image": "작성자 이미지 링크",
    "liek": 12,
    "view": 12,
    "comment": [
        {
            "user_id": 12,
            "user_profile": "image",
            "user_nickname": "이름",
            "comment_data": 2001,
            "comment": "댓글"
        },
    ]
}

# 게시글 작성
{
    "titel": "제목",
    "content": "게시글 내용",
    "image_url": "이미지 링크" 
}

# 게시글 삭제
{

}

# 좋아요

# 좋아요 취소

# 댓긋 잘성
{
    "post_id": 12,
    "user_id": 12,
    "content": "내용"
}

# 댓글 수정
{
    "content": "내용"
}

# 게시글 수정
{
    "title": "제목",
    "content": "내용",
    "image_url": "이미지 링크" 
}
# 회원 정보 수정
{
    "nickname": "이름",
    "profile_image": "url"
}

# 비밀번호 번경
{
    "password": "password"
}