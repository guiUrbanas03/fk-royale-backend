"""Handle xp_event_type requests."""
from flask import Blueprint, jsonify

from source.constants.blueprints import XP_EVENT_TYPE_BLUEPRINT_NAME

xp_event_type_bp = Blueprint(
    XP_EVENT_TYPE_BLUEPRINT_NAME,
    __name__,
    url_prefix=f"/{XP_EVENT_TYPE_BLUEPRINT_NAME}",
)


@xp_event_type_bp.route("/")
def xp_event_type_index():
    """Index request."""
    return jsonify({"data": "XP Event Type"})
