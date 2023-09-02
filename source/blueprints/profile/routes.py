"""Handle profile requests."""
from flask import Blueprint, jsonify

from source.constants.blueprints import PROFILE_BLUEPRINT_NAME

profile_bp = Blueprint(PROFILE_BLUEPRINT_NAME, __name__, url_prefix=f"/{PROFILE_BLUEPRINT_NAME}")


@profile_bp.route("/")
def profile_index():
    """Index request."""
    return jsonify({"data": "Profile"})
