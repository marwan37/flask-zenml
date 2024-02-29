#  Copyright (c) ZenML GmbH 2024. All Rights Reserved.
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
import requests
from flask import current_app as app
from app.utils.global_config import fetch_global_configuration


def call_zenml_api(endpoint, method='get', data=None, params=None):
    """
    Calls a specified ZenML API endpoint.

    Parameters:
        endpoint (str): The API endpoint to call.
        method (str): HTTP method to use for the call. Defaults to 'get'.
        data (dict): Optional JSON data to send in the body of the request.
        params (dict): Optional parameters to append to the URL.

    Returns:
        The JSON response from the API call.
    """
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
    """
    Fetches the API token from ZenML's global configuration.

    Returns:
        The API token as a string.

    Raises:
        ValueError: If the API token is missing in ZenML's global configuration.
    """
    global_config = fetch_global_configuration()
    api_token = global_config.get("store", {}).get("api_token")
    if not api_token:
        raise ValueError("API token is missing in ZenML's global configuration.")
    return api_token
