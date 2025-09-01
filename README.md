# Тестирование API `/v1/favorites`

## Описание
Этот проект предназначен для автоматизированного тестирования ручки **`/v1/favorites`**.
Для выполнения запроса требуется сессионный токен (`token`), получаемый через `/v1/auth/tokens`.

---

## Предусловия
1. Python 3.9

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt

3. Запустить тесты
   ```bash
   pytest tests/
   
4. Открыть отчет allure:

    4.1. Для Windows:
   ```bash
   allure serve .\reports\allure_results

   