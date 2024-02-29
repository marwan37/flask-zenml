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
from app.utils.zen_client import call_zenml_api

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/", methods=["GET"])
def list_users():
    response = call_zenml_api("users", method="get")
    return jsonify(response), response.status_code


@bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    response = call_zenml_api(f"users/{user_id}", method="get")
    return jsonify(response), response.status_code
