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
from flask import Blueprint, jsonify
from app.utils.zen_client import get_zenml_api_token

bp = Blueprint("zen_store", __name__, url_prefix="/zen_store")


@bp.route('/api_token', methods=['GET'])
def get_api_token():
    api_token = get_zenml_api_token()
    if not api_token:
        return jsonify({"error": "API token is missing in ZenML's global configuration."}), 404
    return jsonify({"api_token": api_token})