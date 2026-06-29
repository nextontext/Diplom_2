import allure
import requests

from urls import LOGIN_USER
from messages import INVALID_LOGIN_OR_PASSWORD

class TestLoginUser:

    @allure.epic("Логин пользователя")
    @allure.title("Успешный логин существующего пользователя")
    def test_login_existing_user_success(self, create_user):
        login_data = {
            "email": create_user["email"],
            "password": create_user["password"],
        }

        response = requests.post(LOGIN_USER, json=login_data)
        response_body = response.json()

        assert response.status_code == 200
        assert response_body["success"] is True

    @allure.epic("Логин пользователя")
    @allure.title("Ответ успешного логина содержит токены и данные пользователя")
    def test_login_response_contains_user_data_and_tokens(self, create_user):
        login_data = {
            "email": create_user["email"],
            "password": create_user["password"],
        }

        response = requests.post(LOGIN_USER, json=login_data)
        response_body = response.json()

        assert response_body["user"]["email"] == create_user["email"]
        assert response_body["user"]["name"] == create_user["name"]
        assert "accessToken" in response_body
        assert "refreshToken" in response_body

    @allure.epic("Логин пользователя")
    @allure.title("Ошибка при логине с неверным логином и паролем")
    def test_login_with_invalid_email_and_password_returns_error(self, user_data):
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"],
        }

        response = requests.post(LOGIN_USER, json=login_data)

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": INVALID_LOGIN_OR_PASSWORD,
        }
