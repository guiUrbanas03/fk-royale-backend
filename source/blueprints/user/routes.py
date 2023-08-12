"""Handle user requests."""
from flask import Blueprint, abort, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from source.constants.blueprints import USER_BLUEPRINT_NAME
from source.database.instance import db
from source.dtos.game_stats import CreateGameStatsDTO, GameStatsResourceDTO
from source.dtos.profile import CreateProfileDTO, ProfileResourceDTO
from source.dtos.user import CreateUserDTO, UserResourceDTO
from source.errors.json_error import CauseTypeError
from source.lib.responses import DataResponse

from ..game_stats.services import create_new_game_stats
from ..profile.services import create_new_profile
from .services import create_new_user

user_bp = Blueprint(USER_BLUEPRINT_NAME, __name__, url_prefix=f"/{USER_BLUEPRINT_NAME}")


@user_bp.route("/")
def user_index():
    """Index request."""
    return jsonify({"data": "User"})


@user_bp.route("/create", methods=["POST"])
def create_user():
    data = request.json

    try:
        user_data = CreateUserDTO().load(data["user"])
        user = create_new_user(db.session, user_data)

        profile_data = CreateProfileDTO().load({**data["profile"], "user_id": user.id})
        profile = create_new_profile(db.session, profile_data)

        game_stats_data = CreateGameStatsDTO().load({"profile_id": profile.id})
        game_stats = create_new_game_stats(db.session, game_stats_data)

    except ValidationError as error:
        db.session.rollback()
        abort(422, {"type": CauseTypeError.VALIDATION_ERROR.value, "data": error.messages})

    except ValueError as error:
        db.session.rollback()
        abort(409, {"type": CauseTypeError.DATA_VIOLATION_ERROR.value, "data": str(error)})

    except SQLAlchemyError as error:
        db.session.rollback()
        abort(500, {"type": CauseTypeError.DATABASE_ERROR.value, "data": str(error)})

    db.session.commit()

    return DataResponse(
        "User created succesfully",
        201,
        {
            "user": UserResourceDTO().dump(user),
            "profile": ProfileResourceDTO().dump(profile),
            "game_stats": GameStatsResourceDTO().dump(game_stats),
        },
    ).json()
