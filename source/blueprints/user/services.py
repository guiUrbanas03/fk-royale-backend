import bcrypt
from typing import Union
from uuid import uuid4
from flask_jwt_extended import current_user

from source.dtos.user import CreateUserDTO
from source.models.user.user import User


def get_user_by_id(id: str) -> Union[User, None]:
    """Get user from database filtered by id.

    Parameters
    ----------
    id: str (UUID)

    Returns
    -------
    (User | None)
    """
    return User.query.filter_by(id=id).one_or_none()


def get_user_by_email(email: str) -> Union[User, None]:
    """Get user from database filtered by email.

    Parameters
    ----------
    email: str

    Returns
    -------
    (User | None)
    """

    return User.query.filter_by(email=email).one_or_none()


def create_new_user(session, user_data: CreateUserDTO) -> Union[User, None]:
    """Create new user in the database.

    Parameters
    ----------
    user_data: CreateUserDTO

    Returns
    -------
    (User | None)

    Raises
    ------
    Value error: User with this email address already exists
    """

    if get_user_by_email(user_data["email"]):
        raise ValueError("User with this email address already exists")

    user = User(
        id=uuid4(),
        email=user_data["email"],
        password=hash_password(user_data["password"]),
    )

    session.add(user)
    session.flush()

    return user


def hash_password(password: str) -> bytes:
    """Hash password.

    Parameters
    ----------
    password: str

    Returns
    -------
    bytes
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_user_credentials(email: str, password: str) -> Union[User, None]:
    """Verify if user exists on the database and if its credentials are
    correct.

    Parameters
    ----------
    email: str
    password: str

    Returns
    -------
    (User | None)

    Raises
    ------
    Value Error: Invalid credentials
    """
    user = get_user_by_email(email)

    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password):
        raise ValueError("Invalid credentials")

    return user

def verify_password(current_password: str, new_password: str, confirm_password: str) -> str:
    if not bcrypt.checkpw(current_password.encode("utf-8"), current_user.password):
        raise ValueError("Invalid credentials")
    
    if new_password != confirm_password:
        raise ValueError("Passwords don't match")

    if bcrypt.checkpw(new_password.encode("utf-8"), current_user.password):
        raise ValueError("Password is the same as the old password")

    return hash_password(new_password)