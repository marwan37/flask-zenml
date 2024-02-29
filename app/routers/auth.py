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
from flask import Blueprint, request, jsonify
from app.utils.zen_client import call_zenml_api

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    response = call_zenml_api("auth/login", method="post", data=data)
    return jsonify(response), response.status_code


@bp.route("/device_authorization", methods=["POST"])
def device_authorization():
    client_id = request.json.get("client_id")
    data = {"client_id": client_id}
    response = call_zenml_api("device_authorization", method="post", data=data)
    return jsonify(response)


@bp.route("/logout", methods=["POST"])
def logout():
    response = call_zenml_api("auth/logout", method="post")
    return jsonify(response), response.status_code


@bp.route("/api_token", methods=["POST"])
def api_token():
    data = {
        "pipeline_id": request.json.get("pipeline_id", None),
        "schedule_id": request.json.get("schedule_id", None),
        "expires_minutes": request.json.get("expires_minutes", None),
    }
    response = call_zenml_api("auth/api_token", method="get", params=data)
    return jsonify(response), response.status_code
