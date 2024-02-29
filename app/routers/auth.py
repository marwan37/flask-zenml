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
