import requests

from config import config

BASE_URL = config.server_url.get_secret_value()


def verify_auth(api_key: str) -> bool:
    response = requests.get(f"{BASE_URL}/greenhouse/?api_key={api_key}")
    return response.status_code == 200
