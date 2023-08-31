"""Handle profile requests."""
from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from marshmallow import ValidationError

from source.constants.blueprints import PROFILE_BLUEPRINT_NAME
from source.database.instance import db
from source.dtos.report import CreateReportDTO
from source.errors.json_error import CauseTypeError
from source.lib.responses import DataResponse

from .services import creat_new_report

profile_bp = Blueprint(PROFILE_BLUEPRINT_NAME, __name__, url_prefix=f"/{PROFILE_BLUEPRINT_NAME}")


@profile_bp.route("/")
def profile_index():
    """Index request."""
    return jsonify({"data": "Profile"})


@profile_bp.route("/reports", methods=["POST"])
@jwt_required()
def report_something():
    """Allow the user to report a bug or make a suggestion."""
    try:
        data = request.json
        report_data = CreateReportDTO().load({**data, "profile_id": current_user.profile.id})
        creat_new_report(db.session, report_data)
        db.session.commit()

    except ValidationError as error:
        db.session.rollback()
        abort(422, {"type": CauseTypeError.VALIDATION_ERROR.value, "data": error.messages})

    return DataResponse(
        "Report created succesfully",
        200,
        {
            "category": report_data["category"],
            "subject": report_data["subject"],
            "description": report_data["description"],
        },
    ).json()
