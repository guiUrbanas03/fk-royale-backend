from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from source.constants.blueprints import REPORT_BLUEPRINT_NAME
from source.database.instance import db
from source.dtos.report import CreateReportDTO, ReportResourceDTO
from source.errors.json_error import CauseTypeError
from source.lib.responses import DataResponse
from source.models.report.report import Report

from .services import creat_new_report

report_bp = Blueprint(REPORT_BLUEPRINT_NAME, __name__, url_prefix=f"/{REPORT_BLUEPRINT_NAME}")


@report_bp.route("/")
def report_index():
    """Index request."""
    return jsonify({"data": "Report"})


@report_bp.route("/reports", methods=["POST"])
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


@report_bp.route("/report_bt_profile_id/<profile_id>")
def get_report_by_profile_id(profile_id):
    """Take all the reports from a specific profile ID."""
    try:
        profile_id_from_table = Report.query.filter(Report.profile_id == profile_id)
        data_reports = ReportResourceDTO(many=True).dump(profile_id_from_table)

    except SQLAlchemyError as error:
        db.session.rollback()
        abort(500, {"type": CauseTypeError.DATABASE_ERROR.value, "data": str(error)})

    return DataResponse(
        "Get reports by profile_id successfully",
        200,
        {"all_profile_reports": data_reports},
    ).json()
