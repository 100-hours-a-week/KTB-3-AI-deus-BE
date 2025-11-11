Fast API로 구현하는 커뮤니티 백엔드

## 설치

```bash
# 개발 의존성 설치
pip install -r requirements-dev.txt
```

## 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest test/test_login.py

# 상세 출력
pytest -v

# 특정 테스트만 실행
pytest test/test_login.py::TestLoginAPI::test_login_success
```

## 서버 실행

```bash
uvicorn src.main:app --reload
```