import allure
import pytest
import requests

from helpers import generate_user
from urls import USER
from messages import USER_SHOULD_BE_AUTHORISED


class TestUpdateUser:

    @allure.epic("Изменение данных пользователя")
    @allure.title("Авторизованный пользователь может изменить email")
    def test_authorized_user_can_update_email(self, create_user):
        new_user_data = generate_user()
        updated_data = {
            "email": new_user_data["email"],
        }

        response = requests.patch(
            USER,
            json=updated_data,
            headers={"Authorization": create_user["access_token"]},
        )
        response_body = response.json()

        assert response.status_code == 200
        assert response_body["success"] is True

    @allure.epic("Изменение данных пользователя")
    @allure.title("Авторизованный пользователь может изменить name")
    def test_authorized_user_can_update_name(self, create_user):
        new_user_data = generate_user()
        updated_data = {
            "name": new_user_data["name"],
        }

        response = requests.patch(
            USER,
            json=updated_data,
            headers={"Authorization": create_user["access_token"]},
        )
        response_body = response.json()

        assert response.status_code == 200
        assert response_body["success"] is True

    @allure.epic("Изменение данных пользователя")
    @allure.title("Авторизованный пользователь может изменить password")
    def test_authorized_user_can_update_password(self, create_user):
        new_user_data = generate_user()
        updated_data = {
            "password": new_user_data["password"],
        }

        response = requests.patch(
            USER,
            json=updated_data,
            headers={"Authorization": create_user["access_token"]},
        )
        response_body = response.json()

        assert response.status_code == 200
        assert response_body["success"] is True

    @allure.epic("Изменение данных пользователя")
    @allure.title("Неавторизованный пользователь не может изменить данные")
    @pytest.mark.parametrize("field", ["email", "name", "password"])
    def test_unauthorized_user_can_not_update_any_field(self, field):
        new_user_data = generate_user()
        updated_data = {
            field: new_user_data[field],
        }

        response = requests.patch(USER, json=updated_data)

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": USER_SHOULD_BE_AUTHORISED,
        }
