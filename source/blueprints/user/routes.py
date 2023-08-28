"""Handle user requests."""
from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError


from source.constants.blueprints import USER_BLUEPRINT_NAME
from source.database.instance import db
from source.dtos.game_stats import CreateGameStatsDTO, GameStatsResourceDTO
from source.dtos.profile import CreateProfileDTO, ProfileResourceDTO, UpdateProfileDTO
from source.dtos.user import CreateUserDTO, UserResourceDTO, UserChangePasswordDTO
from source.errors.json_error import CauseTypeError
from source.lib.responses import DataResponse

from ..game_stats.services import create_new_game_stats
from ..profile.services import create_new_profile
from .services import create_new_user, verify_password, user_deletion

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


@user_bp.route("/update", methods=["PUT"])
@jwt_required()
def edit_user():
    """Function to update nickname and full_name from user profile."""
    data = request.json
    try:
        update_data = UpdateProfileDTO().load(data)
        current_user.profile.nickname = update_data["nickname"]
        current_user.profile.full_name = update_data["full_name"]
        db.session.commit()

    except ValidationError as error:
        db.session.rollback()
        abort(422, {"type": CauseTypeError.VALIDATION_ERROR.value, "data": error.messages})

    except SQLAlchemyError as error:
        db.session.rollback()
        abort(500, {"type": CauseTypeError.DATABASE_ERROR.value, "data": str(error)})
    

    return DataResponse(
        "User updated succesfully",
        200,
        {
            "nickname": data["nickname"],
            "full_name": data["full_name"]
        },
    ).json()


@user_bp.route("/change_password", methods=["PUT"])
@jwt_required()
def change_password():
    """Receive the current password(to security change) and the new one."""
    data = request.json

    try:
        password_data = UserChangePasswordDTO().load(data)
        new_password = verify_password(password_data["old_password"], password_data["new_password"], password_data["confirm_new_password"])
        current_user.password = new_password
        db.session.commit()

    except ValidationError as error:
        db.session.rollback()
        abort(422, {"type": CauseTypeError.VALIDATION_ERROR.value, "data": error.messages})

    except ValueError as error:
        db.session.rollback()
        abort(422, {"type": CauseTypeError.VALIDATION_ERROR.value, "data": str(error)})

    return DataResponse(
        "User password updated succesfully",
        200,
        {
        },
    ).json()


@user_bp.route("/delete_account", methods=["DELETE"]) 
@jwt_required()
def delete_user():
    """Allow the user to delete his own account"""

    try:
        if not current_user.deleted_at:
            user_deletion()
            db.session.commit()
            
        else:   
           abort(409, {"type": CauseTypeError.DATA_VIOLATION_ERROR.value, "data": "User already deleted."})

    except ValueError as error:
        db.session.rollback()
        abort(422, {"type": CauseTypeError.VALIDATION_ERROR.value, "data": str(error)})
        
    return DataResponse(
        "User deletion succesfully",
        200,
        {
            "user": "deleted",
            "profile": "deleted",
            "game_stats": "deleted",
        },
    ).json()


