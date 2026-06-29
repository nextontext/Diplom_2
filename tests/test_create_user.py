import pytest
import requests
import allure

from urls import REGISTER_USER
from messages import USER_ALREADY_EXISTS, REQUIRED_FIELDS_MISSING


class TestCreateUSER:

    @allure.epic("Создание пользователя")
    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, registered_user):
        response, _ = registered_user

        response_body = response.json()

        assert response.status_code == 200
        assert response_body["success"] is True
        assert "accessToken" in response_body
        assert "refreshToken" in response_body
    
    @allure.epic("Создание пользователя")
    @allure.title("Пользователь уже зарегистрирован на платформе")
    def test_create_existing_user_returns_error(self, registered_user):
        _, user_data = registered_user

        second_response = requests.post(REGISTER_USER, json=user_data)
        response_body = second_response.json()

        assert second_response.status_code == 403
        assert response_body["success"] is False
        assert response_body["message"] == USER_ALREADY_EXISTS
    
    @allure.epic("Создание пользователя")
    @allure.title("Нельзя создать пользователя без обязательных полей")
    @pytest.mark.parametrize("required_field", ["email", "password", "name"])
    def test_create_user_without_required_field_returns_error(self, user_data, required_field):
        user_data.pop(required_field)

        response = requests.post(REGISTER_USER, json=user_data)
        response_body = response.json()

        assert response.status_code == 403
        assert response_body["success"] is False
        assert response_body["message"] == REQUIRED_FIELDS_MISSING
