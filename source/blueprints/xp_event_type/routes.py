"""Handle xp_event_type requests."""
from flask import Blueprint, jsonify

from source.constants.blueprints import XP_EVENT_TYPE_BLUEPRINT_NAME
from source.models.xp_event_type.xp_event_type import XpEventType
from source.dtos.xp_event_type import XpEventTypeResourceDTO
from source.lib.responses import DataResponse

xp_event_type_bp = Blueprint(
    XP_EVENT_TYPE_BLUEPRINT_NAME,
    __name__,
    url_prefix=f"/{XP_EVENT_TYPE_BLUEPRINT_NAME}",
)


@xp_event_type_bp.route("/")
def xp_event_type_index():
    """Index request."""
    return jsonify({"data": "XP Event Type"})

    
@xp_event_type_bp.route("/xp_events")
def read_xp_event():
    """Get all the XP event types."""

    events = XpEventType.query.all()
    data = XpEventTypeResourceDTO(many=True).dump(events)
    
    return DataResponse(
        "XP event types found successfully",
        200,
        {
           "xp_event_types" : data
        },
    ).json()
