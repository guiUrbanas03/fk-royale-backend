"""Module to handle XpEventType seeders."""
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Final, List
from uuid import uuid4

from source.models.xp_event_type.xp_event_type import XpEventType, XpEventTypeName


def generate_xp_event_type_dict(event_name: str, xp_amount: int, message: str) -> dict:
    """Generates xp event type dict.

    Parameters
    ----------
    event_name: str
    xp_amount: int,
    message: str

    Returns
    -------
    dict
    """
    return {"event_name": event_name, "xp_amount": xp_amount, "message": message}


def seed_xp_event_type(session: Session):
    """Seed initial xp event types.

    Parameters
    ----------
    session: Session

    Raises
    ------
    SQLAlchemyError
    """
    INITIAL_XP_EVENT_TYPES: Final[List[dict]] = [
        generate_xp_event_type_dict(
            XpEventTypeName.WIN_MATCH.value, 50, "Congratulations, you won a match!"
        ),
        generate_xp_event_type_dict(
            XpEventTypeName.WIN_ROUND.value, 20, "Congratulations, you won a round!"
        ),
        generate_xp_event_type_dict(
            XpEventTypeName.WIN_TURN.value, 5, "Congratulations, you won a turn!"
        ),
        generate_xp_event_type_dict(
            XpEventTypeName.FINISH_MATCH.value, 25, "Well done, Match complete!"
        ),
        generate_xp_event_type_dict(XpEventTypeName.FINISH_ROUND.value, 5, "Round over!"),
    ]

    try:
        for xp_event_type_dict in INITIAL_XP_EVENT_TYPES:
            xp_event_type = XpEventType(id=uuid4(), **xp_event_type_dict)

            session.add(xp_event_type)

    except SQLAlchemyError as error:
        session.rollback()
        logging.error(f"Error seeding xp event types: {error}")

    session.commit()
