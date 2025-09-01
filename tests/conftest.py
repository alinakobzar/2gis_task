import pytest
import requests
from api_client.api_client import APIClient
from settings.settings import Settings as St

@pytest.fixture
def api_client():
    """Фикстура для создания клиента API с базовым URL"""
    return APIClient(St.BASE_URL)


@pytest.fixture
def post_token(api_client):
    """Фикстура для получения токена"""
    token = api_client.post(St.ENDPOINT_POST_TOKENS)
    assert token.status_code == 200, "Не удалось получить токен"
    return token.cookies.get("token")
