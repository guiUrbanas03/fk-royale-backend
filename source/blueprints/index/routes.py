"""Define index blueprint."""
from flask import Blueprint, jsonify

from source.constants.blueprints import INDEX_BLUEPRINT_NAME

index_bp = Blueprint(INDEX_BLUEPRINT_NAME, __name__)


@index_bp.route("/")
def index_page():
    """Define index route."""
    return jsonify({"data": "Index"})
