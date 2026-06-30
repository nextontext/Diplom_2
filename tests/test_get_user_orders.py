import allure
import requests

from urls import ORDERS
from messages import USER_SHOULD_BE_AUTHORISED


class TestGetUserOrders:

    @allure.epic("Получение заказов пользователя")
    @allure.title("Авторизованный пользователь может получить свои заказы")
    def test_authorized_user_can_get_orders(self, create_user):
        response = requests.get(
            ORDERS,
            headers={"Authorization": create_user["access_token"]},
        )
        response_body = response.json()

        assert response.status_code == 200
        assert response_body["success"] is True
    
    @allure.epic("Получение заказов пользователя")
    @allure.title("Ответ со списком заказов содержит данные о заказах и счётчиках")
    def test_get_user_orders_response_contains_orders_data(self, create_user):
        response = requests.get(
            ORDERS,
            headers={"Authorization": create_user["access_token"]},
        )
        response_body = response.json()

        assert "orders" in response_body
        assert "total" in response_body
        assert "totalToday" in response_body

    @allure.epic("Получение заказов пользователя")
    @allure.title("Неавторизованный пользователь не может получить свои заказы")
    def test_unauthorized_user_can_not_get_orders(self):
        response = requests.get(ORDERS)

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": USER_SHOULD_BE_AUTHORISED,
        }
