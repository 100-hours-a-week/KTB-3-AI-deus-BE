from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from routers import user, post

# ================ 앱 ==================================
app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # request 파라미터는 FastAPI가 요구하지만 사용하지 않음
    errors = exc.errors()
    if errors:
        err = errors[0]
        # ctx에서 실제 에러 메시지 추출
        error_msg = err.get('msg', '')
        if 'ctx' in err and 'error' in err['ctx']:
            # ValueError의 실제 메시지 추출
            error_msg = str(err['ctx']['error'])

        return JSONResponse(
            status_code=422,
            content={
                "error": "요청 데이터가 올바르지 않습니다",
                "type": err.get('type', 'validation_error'),
                "loc": err.get('loc', []),
                "details": error_msg
            }
        )

    # 에러가 없는 경우 기본 응답
    return JSONResponse(
        status_code=422,
        content={
            "error": "요청 데이터가 올바르지 않습니다",
            "type": "validation_error",
            "loc": [],
            "details": "Unknown validation error"
        }
    )

# Pydantic ValidationError도 동일하게 처리
@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    err = exc.errors()[0]
    return JSONResponse(
        status_code=422,
        content={
            "error": "요청 데이터가 올바르지 않습니다",
            "type": err['type'],
            "loc": err['loc'],
            "msg": err['msg']
        }
    )

# 라우터 등록은 exception handler 이후에
app.include_router(user.router)
app.include_router(post.router)
