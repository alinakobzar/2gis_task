import requests

class APIClient:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.timeout = timeout

    def post(self, endpoint, data=None, cookies=None, as_json=None):
        if as_json:
            # Отправляем как JSON
            response = requests.post(f"{self.base_url}/{endpoint}", json=data, cookies=cookies, timeout=self.timeout)
        else:
            # Отправляем как x-www-form-urlencoded
            response = requests.post(f"{self.base_url}/{endpoint}", data=data, cookies=cookies, timeout=self.timeout)
        return response