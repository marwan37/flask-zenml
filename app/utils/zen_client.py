import requests
from flask import current_app as app
from app.utils.global_config import fetch_global_configuration


def call_zenml_api(endpoint, method='get', data=None, params=None):
    """Generic function to call ZenML API endpoints."""
    base_url = app.config['ZENML_API_URL']
    url = f"{base_url}/{endpoint}"
    api_token = get_zenml_api_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {api_token}",
    }

    response = requests.request(method, url, json=data, params=params, headers=headers)
    return response.json()


def get_zenml_api_token():
    global_config = fetch_global_configuration()
    api_token = global_config.get("store", {}).get("api_token")
    if not api_token:
        raise ValueError("API token is missing in ZenML's global configuration.")
    return api_token
