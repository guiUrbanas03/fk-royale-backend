"""Handle auth requests."""
from flask import Blueprint, abort, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    current_user,
    get_jwt,
    jwt_required,
)
from marshmallow import ValidationError

from source.blueprints.auth.services import create_revoked_token, get_revoked_token_by_token
from source.blueprints.user.services import get_user_by_id, verify_user_credentials
from source.constants.blueprints import AUTH_BLUEPRINT_NAME
from source.dtos.auth import LoginUserDTO
from source.dtos.revoked_token import CreateRevokedTokenDTO, RevokedTokenResourceDTO
from source.errors.json_error import CauseTypeError, jwt_error
from source.jwt.instance import jwt
from source.jwt.jwt_causes import JwtCause
from source.lib.responses import DataResponse
from source.models.user.user import User

auth_bp = Blueprint(AUTH_BLUEPRINT_NAME, __name__, url_prefix=f"/{AUTH_BLUEPRINT_NAME}")


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Refresh jwt tokens."""
    access_token = create_access_token(identity=current_user)
    return DataResponse("Token refreshed successfully", 201, {"access_token": access_token}).json()


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user by generating JWT tokens."""
    data = request.json

    try:
        user_data = LoginUserDTO().load(data)
        user = verify_user_credentials(user_data["email"], user_data["password"])

        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)

        return DataResponse(
            "User authenticated successfully",
            201,
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user.resource,
                "profile": user.profile.resource,
                "game_stats": user.profile.game_stats.resource,
            },
        ).json()

    except ValidationError as error:
        abort(422, {"type": CauseTypeError.VALIDATION_ERROR.value, "data": error.messages})

    except ValueError as error:
        abort(400, {"type": CauseTypeError.DATA_VIOLATION_ERROR.value, "data": str(error)})


@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout():
    """Logout user by revoking their tokens."""
    try:
        token_data = get_jwt()

        token_dto = CreateRevokedTokenDTO().load(
            {"user_id": token_data["sub"], "token": token_data["jti"], "type_": token_data["type"]}
        )

        revoked_token = create_revoked_token(token_dto)

    except ValidationError as error:
        abort(422, {"type": CauseTypeError.VALIDATION_ERROR.value, "data": error.messages})

    return DataResponse(
        "Token revoked successfully",
        201,
        {
            "revoked_token": RevokedTokenResourceDTO().dump(revoked_token),
        },
    ).json()


@auth_bp.route("/who-am-i", methods=["GET"])
@jwt_required()
def who_am_i():
    """Get current logged in user."""
    return DataResponse(
        "User retrieved successfully",
        200,
        {
            "user": current_user.resource,
            "profile": current_user.profile.resource,
            "game_stats": current_user.profile.game_stats.resource,
        },
    ).json()


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> str:
    """Takes the identity object when creating JWTs
    and converts it to a JSON serializable format.

    Parameters
    ----------
    user: User

    Returns
    -------
    str
    """
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header: dict, jwt_data: dict) -> User:
    """Loads user from the database whenever a protected route is accessed.

    Parameters
    ----------
    jwt_header: dict
    jwt_data: dict

    Returns
    -------
    User
    """
    return get_user_by_id(jwt_data["sub"])


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Expired token loader response.

    Parameters
    ----------
    jwt_header: dict
    jwt_data: dict

    Returns
    -------
    Response
    """
    if jwt_payload["type"] == "refresh":
        return jwt_error(JwtCause.REFRESH_TOKEN_EXPIRED.value)
    return jwt_error(JwtCause.ACCESS_TOKEN_EXPIRED.value)


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Invalid token loader response.

    Parameters
    ----------
    error: str

    Returns
    -------
    Response
    """
    return jwt_error(JwtCause.INVALID_TOKEN.value)


@jwt.token_verification_failed_loader
def token_failed_callback(jwt_header, jwt_payload):
    """Token failed loader response.

    Parameters
    ----------
    jwt_header: dict
    jwt_data: dict

    Returns
    -------
    Response
    """
    return jwt_error(JwtCause.TOKEN_FAILED.value)


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(jwt_header, jwt_payload):
    """Needs fresh token loader response.

    Parameters
    ----------
    jwt_header: dict
    jwt_data: dict

    Returns
    -------
    Response
    """
    return jwt_error(JwtCause.NEEDS_FRESH_TOKEN.value)


@jwt.unauthorized_loader
def missing_token_callback(error):
    """Missing token loader response.

    Parameters
    ----------
    error: str

    Returns
    -------
    Response
    """
    return jwt_error(JwtCause.MISSING_TOKEN.value)


@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    """Check if token is revoked.

    Parameters
    ----------
    jwt_header: dict
    jwt_data: dict

    Returns
    -------
    bool
    """
    jti = jwt_payload["jti"]
    get_revoked_token_by_token(jti)
    return False


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    """Revoked token loader response.

    Parameters
    ----------
    jwt_header: dict
    jwt_data: dict

    Returns
    -------
    Response
    """
    return jwt_error(JwtCause.REVOKED_TOKEN.value)
