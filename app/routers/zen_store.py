from flask import Blueprint, jsonify
from app.utils.zen_client import get_zenml_api_token

bp = Blueprint("zen_store", __name__, url_prefix="/zen_store")


@bp.route('/api_token', methods=['GET'])
def get_api_token():
    api_token = get_zenml_api_token()
    if not api_token:
        return jsonify({"error": "API token is missing in ZenML's global configuration."}), 404
    return jsonify({"api_token": api_token})