import pytest
import requests

from helpers import generate_user
from urls import REGISTER_USER, USER, INGREDIENTS


@pytest.fixture
def user_data():
    return generate_user()


@pytest.fixture
def create_user(user_data):
    response = requests.post(REGISTER_USER, json=user_data)
    response_body = response.json()

    yield {
        "email": user_data["email"],
        "password": user_data["password"],
        "name": user_data["name"],
        "access_token": response_body["accessToken"],
        "refresh_token": response_body["refreshToken"],
    }

    requests.delete(USER, headers={"Authorization": response_body["accessToken"]},)


@pytest.fixture
def registered_user(user_data):
    response = requests.post(REGISTER_USER, json=user_data)
    response_body = response.json()

    yield response, user_data

    requests.delete(
        USER,
        headers={"Authorization": response_body["accessToken"]},
    )


@pytest.fixture
def ingredients():
    response = requests.get(INGREDIENTS)
    response_body = response.json()

    return [
        response_body["data"][0]["_id"],
        response_body["data"][1]["_id"],
    ]
