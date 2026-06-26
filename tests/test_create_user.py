import pytest
import requests
import allure

from urls import REGISTER_USER


class TestCreateUSER:

    @allure.epic("Создание пользователя")
    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, user_data):
        response = requests.post(REGISTER_USER, json=user_data)

        print(response)

        response_body = response.json()

        assert response.status_code == 200
        assert response_body["success"] is True
        assert response_body["user"]["email"] == user_data["email"]
        assert response_body["user"]["name"] == user_data["name"]
        assert "accessToken" in response_body
        assert "refreshToken" in response_body
    
    @allure.epic("Создание пользователя")
    @allure.title("Пользователь уже зарегистрирован на платформе")
    def test_create_existing_user_returns_error(self, user_data):
        first_response = requests.post(REGISTER_USER, json=user_data)
        second_response = requests.post(REGISTER_USER, json=user_data)

        assert first_response.status_code == 200
        assert second_response.status_code == 403
    
    @allure.epic("Создание пользователя")
    @allure.title("Нельзя создать пользователя без обязательных полей")
    @pytest.mark.parametrize("required_field", ["email", "password", "name"])
    def test_create_user_without_required_field_returns_error(self, user_data, required_field):
        user_data.pop(required_field)

        response = requests.post(REGISTER_USER, json=user_data)

        assert response.status_code == 403
