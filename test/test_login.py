import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app


client = TestClient(app)


class TestLoginAPI:
    """로그인 API 테스트"""

    # ================== 성공 테스트 =========================
    def test_login_success(self):
        """정상적인 로그인 테스트"""

        response = client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "Test1234!"
            }
        )

        assert response.status_code == 200
        assert response.json() == {
            "email": "test@example.com",
            "password": "Test1234!",
            "nickname": "test",
            "user_profile_image_url": "image_storage/test"
        }

    @pytest.mark.parametrize("email,password", [
        ("user@test.com", "Valid123!"),
        ("admin@company.co.kr", "Admin2024@"),
        ("test.user+tag@example.org", "MyP@ssw0rd"),
    ])
    def test_login_various_valid_formats(self, email, password):
        """다양한 유효한 형식 테스트"""
        mock_user = {"id": 1, "email": email}

        with patch("main.authenticate_user", return_value=mock_user):
            response = client.post(
                "/login",
                json={"email": email, "password": password}
            )

        assert response.status_code == 200


    # ================== 싪 테스트 =========================
    def test_login_fail_wrong_credentials(self):
        """없는 인증 정보로 로그인 실패"""
        with patch("main.authenticate_user", return_value=None):
            response = client.post(
                "/login",
                json={
                    "email": "wrong@example.com",
                    "password": "Wrong1234!"
                }
            )

        assert response.status_code == 403
        assert response.json()["detail"] == "fail login"


    def test_login_invalid_email_format(self):
        """잘못된 이메일 형식"""
        response = client.post(
            "/login",
            json={
                "email": "invalid-email",  # @ 없음
                "password": "Test1234!"
            }
        )

        assert response.status_code == 422
        assert "error" in response.json()
        assert "요청 데이터가 올바르지 않습니다" in response.json()["error"]


    def test_login_invalid_password_format(self):
        """잘못된 비밀번호 형식 - 특수문자 없음"""
        response = client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "Test1234"  # 특수문자 없음
            }
        )

        assert response.status_code == 422
        assert "error" in response.json()


    def test_login_password_too_short(self):
        """비밀번호 길이 부족 (8자 미만)"""
        response = client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "Ts1!"  # 4자
            }
        )

        assert response.status_code == 422
        assert "error" in response.json()


    def test_login_password_too_long(self):
        """비밀번호 길이 초과 (20자 초과)"""
        response = client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "Test1234!Test1234!Extra"  # 21자
            }
        )

        assert response.status_code == 422
        assert "error" in response.json()


    def test_login_missing_email(self):
        """이메일 누락"""
        response = client.post(
            "/login",
            json={
                "password": "Test1234!"
            }
        )

        assert response.status_code == 422
        assert "error" in response.json()


    def test_login_missing_password(self):
        """비밀번호 누락"""
        response = client.post(
            "/login",
            json={
                "email": "test@example.com"
            }
        )

        assert response.status_code == 422
        assert "error" in response.json()


    def test_login_empty_body(self):
        """빈 요청 바디"""
        response = client.post("/login", json={})

        assert response.status_code == 422
        assert "error" in response.json()


    def test_login_password_no_uppercase(self):
        """비밀번호 대문자 없음"""
        response = client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "test1234!"  # 대문자 없음
            }
        )

        assert response.status_code == 422


    def test_login_password_no_lowercase(self):
        """비밀번호 소문자 없음"""
        response = client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "TEST1234!"  # 소문자 없음
            }
        )

        assert response.status_code == 422


    def test_login_password_no_digit(self):
        """비밀번호 숫자 없음"""
        response = client.post(
            "/login",
            json={
                "email": "test@example.com",
                "password": "TestTest!"  # 숫자 없음
            }
        )

        assert response.status_code == 422


    @pytest.mark.parametrize("invalid_email", [
        "notanemail",
        "@example.com",
        "user@",
        "user @example.com",
        "user@.com",
    ])
    def test_login_various_invalid_emails(self, invalid_email):
        """다양한 잘못된 이메일 형식"""
        response = client.post(
            "/login",
            json={
                "email": invalid_email,
                "password": "Test1234!"
            }
        )

        assert response.status_code == 422


