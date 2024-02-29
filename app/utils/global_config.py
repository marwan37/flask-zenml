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
import json

from zenml.config.global_config import GlobalConfiguration
from app.models.user import UserModel
from zenml.config.store_config import StoreConfiguration
from zenml.zen_stores.rest_zen_store import RestZenStoreConfiguration


def fetch_active_user():
    """Fetches the active user."""
    gc = GlobalConfiguration()
    active_user = gc.zen_store.get_user()
    user_model = UserModel(id=active_user.id, name=active_user.name)
    return user_model.json(indent=2)


def fetch_store_info():
    """Fetches store information as a dictionary."""
    gc = GlobalConfiguration()
    return {
        "store_type": gc.store.type,
        "store_url": gc.store.url
    }


def fetch_global_configuration():
    """Fetches the global configuration as a Python dictionary."""
    gc = GlobalConfiguration()
    json_string = gc.json(indent=2)
    return json.loads(json_string)


def set_store_configuration(remote_url: str, access_token: str, user_id: str):
    """Sets the ZenML global configuration to use a remote REST store.

    Args:
        remote_url (str): The URL of the remote ZenML server.
        access_token (str): The access token retrieved via OAuth2 for authentication.
        user_id (str): The ID of the user, fetched from the utility file.
    """
    gc = GlobalConfiguration()
    new_store_config = RestZenStoreConfiguration(
        type="rest",
        url=remote_url,
        api_token=access_token,
        verify_ssl=True
    )

    # gc.store = new_store_config
    # gc.user_id = user_id
    gc.set_store(new_store_config)



