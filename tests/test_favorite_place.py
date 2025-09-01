import allure
import json
import pytest
from datetime import datetime
from settings.settings import Settings as St

@allure.story("Добавление избранного места")
class TestAuthUser:
    @allure.title("Успешное добавление избранного места")
    @allure.description(
        "Проверка, успешного добавление избранного места пользователя, возвращения кода 200 и тела ответа")
    def test_post_favorites_success(self, post_token, api_client):
        payload = {
            "title": "Test",
            "lat": 55.028254,
            "lon": 82.918501
        }
        cookies = {"token": post_token}

        with allure.step("Отправка POST-запроса для добавления избранного места"):
            response = api_client.post(St.ENPOINT_POST_FAVORITES, data=payload, cookies=cookies)

            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что код ответа 200"):
            assert response.status_code == 200, f"Ожидался код 200, получено {response.status_code}"

        body = response.json()

        with allure.step("Проверка тела ответа"):
            assert isinstance(body["id"], int), "id должен быть числом"
            assert body["title"] == payload["title"], "Название места не совпадает"
            assert body["lat"] == float(payload["lat"]), "lat не совпадает"
            assert body["lon"] == float(payload["lon"]), "lon не совпадает"

            if "color" in payload:
                assert body["color"] == payload["color"], "Цвет не совпадает"
            else:
                assert body["color"] is None, "Значение не null"

            with allure.step("Проверка формата created_at (ISO8601)"):
                try:
                    datetime.fromisoformat(body["created_at"].replace("Z", "+00:00"))
                except ValueError:
                    pytest.fail("created_at не соответствует ISO8601")

    @allure.title("Успешное добавление избранного места c цветом")
    @allure.description(
        "Проверка, успешного добавление избранного места с цветом пользователя, возвращения кода 200 и тела ответа")
    def test_post_favorites_with_color_success(self, post_token, api_client):
        payload = {
            "title": "Test",
            "lat": 55.028254,
            "lon": 82.918501,
            "color": "BLUE"
        }
        cookies = {"token": post_token}

        with allure.step("Отправка POST-запроса для добавления избранного места"):
            response = api_client.post(St.ENPOINT_POST_FAVORITES, data=payload, cookies=cookies)

            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что код ответа 200"):
            assert response.status_code == 200, f"Ожидался код 200, получено {response.status_code}"

        body = response.json()

        with allure.step("Проверка тела ответа"):
            assert isinstance(body["id"], int), "id должен быть числом"
            assert body["title"] == payload["title"], "Название места не совпадает"
            assert body["lat"] == float(payload["lat"]), "lat не совпадает"
            assert body["lon"] == float(payload["lon"]), "lon не совпадает"

            if "color" in payload:
                assert body["color"] == payload["color"], "Цвет не совпадает"
            else:
                assert body["color"] is None, "Значение не null"

            with allure.step("Проверка формата created_at (ISO8601)"):
                try:
                    datetime.fromisoformat(body["created_at"].replace("Z", "+00:00"))
                except ValueError:
                    pytest.fail("created_at не соответствует ISO8601")

    @allure.title("Проверка граничных значений поля title")
    @allure.description(
        "Проверка, успешного добавление избранного места с title длиной 1 символ и 1000 символов,"
        " возвращения кода 200 и тела ответа")
    @pytest.mark.parametrize("title_length", [1000, 1])
    def test_post_favorites_boundary_values_accept(self, post_token, api_client, title_length):
        """Найден баг, так как длина 1000 - несоответствие документации"""
        payload = {
            "title": "T"* title_length,
            "lat": 55.028254,
            "lon": 82.918501,
        }
        cookies = {"token": post_token}

        with allure.step("Отправка POST-запроса для добавления избранного места"):
            response = api_client.post(St.ENPOINT_POST_FAVORITES, data=payload, cookies=cookies)

            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что код ответа 200"):
            assert response.status_code == 200, f"Ожидался код 200, получено {response.status_code}"

        body = response.json()

        with allure.step("Проверка тела ответа"):
            assert isinstance(body["id"], int), "id должен быть числом"
            assert len(body["title"]) == title_length
            assert body["title"] == payload["title"], "Название места не совпадает"
            assert body["lat"] == float(payload["lat"]), "lat не совпадает"
            assert body["lon"] == float(payload["lon"]), "lon не совпадает"

            if "color" in payload:
                assert body["color"] == payload["color"], "Цвет не совпадает"
            else:
                assert body["color"] is None, "Значение не null"

            with allure.step("Проверка формата created_at (ISO8601)"):
                try:
                    datetime.fromisoformat(body["created_at"].replace("Z", "+00:00"))
                except ValueError:
                    pytest.fail("created_at не соответствует ISO8601")


    @allure.title("Проверка выхода за граничные значения поля title")
    @allure.description(
        "Проверка, добавление избранного места с title длиной 1001 символов,"
        " возвращения кода 400 и ошибки")
    @pytest.mark.parametrize("title_length", [1001])
    def test_post_favorites_boundary_values_not_accept(self, post_token, api_client, title_length):
        payload = {
            "title": "T"* title_length,
            "lat": 55.028254,
            "lon": 82.918501,
        }
        cookies = {"token": post_token}

        with allure.step("Отправка POST-запроса для добавления избранного места"):
            response = api_client.post(St.ENPOINT_POST_FAVORITES, data=payload, cookies=cookies)

            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что код ответа 400"):
            assert response.status_code == 400, f"Ожидался код 400, получено {response.status_code}"

        with allure.step("Проверка тела ошибки"):
            body = response.json()
            error = body["error"]
            assert "id" in error, "В 'error' нет поля 'id'"
            assert error.get("message") == "Параметр 'title' должен содержать не более 999 символов", \
                    f"Неверный message: {error.get('message')}"

    @allure.title("Проверка пустого значения поля title")
    @allure.description(
        "Проверка, добавление избранного места с пустым title"
        " возвращения кода 400 и ошибки")
    @pytest.mark.parametrize("title_length", [""])
    def test_post_favorites_with_empty_title(self, post_token, api_client, title_length):
        payload = {
            "title": title_length,
            "lat": 55.028254,
            "lon": 82.918501,
        }
        cookies = {"token": post_token}

        with allure.step("Отправка POST-запроса для добавления избранного места"):
            response = api_client.post(St.ENPOINT_POST_FAVORITES, data=payload, cookies=cookies)

            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что код ответа 400"):
            assert response.status_code == 400, f"Ожидался код 400, получено {response.status_code}"

        with allure.step("Проверка тела ошибки"):
            body = response.json()
            error = body["error"]
            assert "id" in error, "В 'error' нет поля 'id'"
            assert error.get("message") == "Параметр 'title' не может быть пустым", \
                    f"Неверный message: {error.get('message')}"


    @allure.title("Проверка граничных значений поля lon")
    @allure.description(
        "Проверка, добавление избранного места с валидными граничными значениями lon"
        " возвращения кода 400 и ошибки")
    @pytest.mark.parametrize("lon", [180.000000, -180.000000, -179.999999, 179.999999])
    def test_post_favorites_with_boundary_accept_lon(self, post_token, api_client, lon):
        payload = {
            "title": "Test",
            "lat": 55.028254,
            "lon": lon,
        }
        cookies = {"token": post_token}

        with allure.step("Отправка POST-запроса для добавления избранного места"):
            response = api_client.post(St.ENPOINT_POST_FAVORITES, data=payload, cookies=cookies)

            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что код ответа 200"):
            assert response.status_code == 200, f"Ожидался код 200, получено {response.status_code}"

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert isinstance(body["id"], int), "id должен быть числом"
            assert body["title"] == payload["title"], "Название места не совпадает"
            assert body["lat"] == float(payload["lat"]), "lat не совпадает"
            assert body["lon"] == float(payload["lon"]), "lon не совпадает"

            if "color" in payload:
                assert body["color"] == payload["color"], "Цвет не совпадает"
            else:
                assert body["color"] is None, "Значение не null"

            with allure.step("Проверка формата created_at (ISO8601)"):
                try:
                    datetime.fromisoformat(body["created_at"].replace("Z", "+00:00"))
                except ValueError:
                    pytest.fail("created_at не соответствует ISO8601")

    @allure.title("Проверка невалидных граничных значений поля lon")
    @allure.description(
        "Проверка, добавление избранного места с невалидными граничными значениями lon"
        " возвращения кода 400 и ошибки")
    @pytest.mark.parametrize("lon", [-180.000001, 180.000001])
    def test_post_favorites_with_boundary_not_accept_lon(self, post_token, api_client, lon):
        payload = {
            "title": "Test",
            "lat": 55.028254,
            "lon": lon,
        }
        cookies = {"token": post_token}

        with allure.step("Отправка POST-запроса для добавления избранного места"):
            response = api_client.post(St.ENPOINT_POST_FAVORITES, data=payload, cookies=cookies)

            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что код ответа 400"):
            assert response.status_code == 400, f"Ожидался код 400, получено {response.status_code}"


        with allure.step("Проверка тела ошибки"):
            body = response.json()
            error = body["error"]
            assert "id" in error, "В 'error' нет поля 'id'"
            if lon == -180.000001:
                assert error.get("message") == "Параметр 'lon' должен быть не менее -180", \
                        f"Неверный message: {error.get('message')}"
            if lon == 180.000001:
                assert error.get("message") == "Параметр 'lon' должен быть не более 180", \
                    f"Неверный message: {error.get('message')}"

    @allure.title("Проверка граничных значений поля lat")
    @allure.description(
        "Проверка, добавление избранного места с валидными граничными значениями lat"
        " возвращения кода 400 и ошибки")
    @pytest.mark.parametrize("lat", [90.000000, -90.000000, -89.999999, 89.999999])
    def test_post_favorites_with_boundary_accept_lat(self, post_token, api_client, lat):
        payload = {
            "title": "Test",
            "lat": lat,
            "lon": 82.918501,
        }
        cookies = {"token": post_token}

        with allure.step("Отправка POST-запроса для добавления избранного места"):
            response = api_client.post(St.ENPOINT_POST_FAVORITES, data=payload, cookies=cookies)

            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что код ответа 200"):
            assert response.status_code == 200, f"Ожидался код 200, получено {response.status_code}"

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert isinstance(body["id"], int), "id должен быть числом"
            assert body["title"] == payload["title"], "Название места не совпадает"
            assert body["lat"] == float(payload["lat"]), "lat не совпадает"
            assert body["lon"] == float(payload["lon"]), "lon не совпадает"

            if "color" in payload:
                assert body["color"] == payload["color"], "Цвет не совпадает"
            else:
                assert body["color"] is None, "Значение не null"

            with allure.step("Проверка формата created_at (ISO8601)"):
                try:
                    datetime.fromisoformat(body["created_at"].replace("Z", "+00:00"))
                except ValueError:
                    pytest.fail("created_at не соответствует ISO8601")

    @allure.title("Проверка невалидных граничных значений поля lat")
    @allure.description(
        "Проверка, добавление избранного места с невалидными граничными значениями lat"
        " возвращения кода 400 и ошибки")
    @pytest.mark.parametrize("lat", [-90.000001, 90.000001])
    def test_post_favorites_with_boundary_not_accept_lat(self, post_token, api_client, lat):
        payload = {
            "title": "Test",
            "lat": lat,
            "lon": 82.918501,
        }
        cookies = {"token": post_token}

        with allure.step("Отправка POST-запроса для добавления избранного места"):
            response = api_client.post(St.ENPOINT_POST_FAVORITES, data=payload, cookies=cookies)

            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что код ответа 400"):
            assert response.status_code == 400, f"Ожидался код 400, получено {response.status_code}"

        with allure.step("Проверка тела ошибки"):
            body = response.json()
            error = body["error"]
            assert "id" in error, "В 'error' нет поля 'id'"
            if lat == -90.000001:
                assert error.get("message") == "Параметр 'lat' должен быть не менее -90", \
                    f"Неверный message: {error.get('message')}"
            if lat == 90.000001:
                assert error.get("message") == "Параметр 'lat' должен быть не более 90", \
                    f"Неверный message: {error.get('message')}"

    @allure.title("Проверка пустого значения поля lat")
    @allure.description(
        "Проверка, добавление избранного места с пустым значениями lat"
        " возвращения кода 400 и ошибки")
    @pytest.mark.parametrize("lat", [None])
    def test_post_favorites_with_empty_lat(self, post_token, api_client, lat):
        payload = {
            "title": "Test",
            "lat": lat,
            "lon": 82.918501,
        }
        cookies = {"token": post_token}

        with allure.step("Отправка POST-запроса для добавления избранного места"):
            response = api_client.post(St.ENPOINT_POST_FAVORITES, data=payload, cookies=cookies)

            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что код ответа 400"):
            assert response.status_code == 400, f"Ожидался код 400, получено {response.status_code}"

        with allure.step("Проверка тела ошибки"):
            body = response.json()
            error = body["error"]
            assert "id" in error, "В 'error' нет поля 'id'"
            assert error.get("message") == "Параметр 'lat' является обязательным", \
                    f"Неверный message: {error.get('message')}"

    @allure.title("Проверка пустого значения поля lon")
    @allure.description(
        "Проверка, добавление избранного места с пустым значениями lon"
        " возвращения кода 400 и ошибки")
    @pytest.mark.parametrize("lon", [None])
    def test_post_favorites_with_empty_lon(self, post_token, api_client, lon):
        payload = {
            "title": "Test",
            "lat": 55.870212,
            "lon": lon,
        }
        cookies = {"token": post_token}

        with allure.step("Отправка POST-запроса для добавления избранного места"):
            response = api_client.post(St.ENPOINT_POST_FAVORITES, data=payload, cookies=cookies)

            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что код ответа 400"):
            assert response.status_code == 400, f"Ожидался код 400, получено {response.status_code}"

        with allure.step("Проверка тела ошибки"):
            body = response.json()
            error = body["error"]
            assert "id" in error, "В 'error' нет поля 'id'"
            assert error.get("message") == "Параметр 'lon' является обязательным", \
                    f"Неверный message: {error.get('message')}"

    @allure.title("Проверка некорректного значения поля color")
    @allure.description(
        "Проверка, добавление избранного места с некорректным значением color"
        " возвращения кода 400 и ошибки")
    @pytest.mark.parametrize("color", ["Purple", "PINK"])
    def test_post_favorites_with_incorrect_color(self, post_token, api_client, color):
        payload = {
            "title": "Test",
            "lat": 55.870212,
            "lon": 81.201920,
            "color": color
        }
        cookies = {"token": post_token}

        with allure.step("Отправка POST-запроса для добавления избранного места"):
            response = api_client.post(St.ENPOINT_POST_FAVORITES, data=payload, cookies=cookies)

            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что код ответа 400"):
            assert response.status_code == 400, f"Ожидался код 400, получено {response.status_code}"

        with allure.step("Проверка тела ошибки"):
            body = response.json()
            error = body["error"]
            assert "id" in error, "В 'error' нет поля 'id'"
            assert error.get("message") == ("Параметр 'color' может быть одним из следующих "
                                            "значений: BLUE, GREEN, RED, YELLOW"), \
                    f"Неверный message: {error.get('message')}"

    @allure.title("Проверка ручки без токена авторизации")
    @allure.description(
        "Проверка, добавление избранного места без токена авторизацииr"
        " возвращения кода 400 и ошибки")
    def test_post_favorites_without_token(self, api_client):
        payload = {
            "title": "Test",
            "lat": 55.870212,
            "lon": 81.201920,
        }

        with allure.step("Отправка POST-запроса для добавления избранного места"):
            response = api_client.post(St.ENPOINT_POST_FAVORITES, data=payload)

            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что код ответа 401"):
            assert response.status_code == 401, f"Ожидался код 401, получено {response.status_code}"

        with allure.step("Проверка тела ошибки"):
            body = response.json()
            error = body["error"]
            assert "id" in error, "В 'error' нет поля 'id'"
            assert error.get("message") == "Параметр 'token' является обязательным", \
                    f"Неверный message: {error.get('message')}"

    @allure.title("Проверка ручки c некорректным токеном авторизации")
    @allure.description(
        "Проверка, добавление избранного места c некорректным токеном авторизацииr"
        " возвращения кода 400 и ошибки")
    def test_post_favorites_with_incorrect_token(self, api_client):
        payload = {
            "title": "Test",
            "lat": 55.870212,
            "lon": 81.201920,
        }
        cookies = {"token": "123"}

        with allure.step("Отправка POST-запроса для добавления избранного места"):
            response = api_client.post(St.ENPOINT_POST_FAVORITES, data=payload, cookies=cookies)

            allure.attach(
                json.dumps(payload, indent=2, ensure_ascii=False),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("Проверка, что код ответа 401"):
            assert response.status_code == 401, f"Ожидался код 401, получено {response.status_code}"

        with allure.step("Проверка тела ошибки"):
            body = response.json()
            error = body["error"]
            assert "id" in error, "В 'error' нет поля 'id'"
            assert error.get("message") == "Передан несуществующий или «протухший» 'token'", \
                    f"Неверный message: {error.get('message')}"