import allure
import requests

from urls import ORDERS


class TestCreateOrder:

    @allure.epic("Создание заказа")
    @allure.title("Авторизованный пользователь может создать заказ с ингредиентами")
    def test_authorized_user_can_create_order_with_ingredients(self, create_user, ingredients):
        order_data = {
            "ingredients": ingredients,
        }

        response = requests.post(
            ORDERS,
            json=order_data,
            headers={"Authorization": create_user["access_token"]},
        )
        response_body = response.json()

        assert response.status_code == 200
        assert response_body["success"] is True
        assert "name" in response_body
        assert "order" in response_body
        assert "number" in response_body["order"]

    @allure.epic("Создание заказа")
    @allure.title("Неавторизованный пользователь может создать заказ с ингредиентами")
    def test_unauthorized_user_can_create_order_with_ingredients(self, ingredients):
        order_data = {
            "ingredients": ingredients,
        }

        response = requests.post(ORDERS, json=order_data)
        response_body = response.json()

        assert response.status_code == 200
        assert response_body["success"] is True
        assert "name" in response_body
        assert "order" in response_body
        assert "number" in response_body["order"]

    @allure.epic("Создание заказа")
    @allure.title("Нельзя создать заказ без ингредиентов")
    def test_create_order_without_ingredients_returns_error(self, create_user):
        order_data = {
            "ingredients": [],
        }

        response = requests.post(
            ORDERS,
            json=order_data,
            headers={"Authorization": create_user["access_token"]},
        )

        assert response.status_code == 400

    @allure.epic("Создание заказа")
    @allure.title("Нельзя создать заказ с неверным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash_returns_error(self, create_user):
        order_data = {
            "ingredients": ["invalid_ingredient_hash"],
        }

        response = requests.post(
            ORDERS,
            json=order_data,
            headers={"Authorization": create_user["access_token"]},
        )

        assert response.status_code == 500
