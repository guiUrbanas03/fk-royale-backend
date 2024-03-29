from flask_jwt_extended import decode_token
from typing import Union
from uuid import uuid4

from source.blueprints.user.services import get_user_by_id
from source.database.instance import db
from source.dtos.revoked_token import CreateRevokedTokenDTO
from source.models.revoked_token.revoked_token import RevokedToken
from source.models.user.user import User


def create_revoked_token(token_data: CreateRevokedTokenDTO) -> RevokedToken:
    """Create new revoked token entry in the database.

    Parameters
    ----------
    token_data: CreateRevokedTokenDTO

    Returns
    -------
    RevokedToken
    """

    revoked_token = RevokedToken(
        id=uuid4(),
        token=token_data["token"],
        user_id=token_data["user_id"],
        type_=token_data["type_"],
    )
    db.session.add(revoked_token)
    db.session.commit()

    return revoked_token


def get_revoked_token_by_token(token: str) -> Union[RevokedToken, None]:
    """Get revoked token from database filtered by token.

    Parameters
    ----------
    token: str

    Returns
    -------
    (RevokedToken|None)
    """
    return RevokedToken.query.filter_by(token=token).one_or_none()


def get_user_by_token(token: str) -> User:
    """Get user from access token.

    Parameters
    ----------
    token: str

    Returns
    -------
    user: User
    """
    decoded_token: dict = decode_token(token)
    return get_user_by_id(decoded_token["sub"])
