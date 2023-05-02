"""Module to handle seeders commands."""
import click
import logging
from sqlalchemy.exc import SQLAlchemyError

from source.constants.tables import XP_EVENT_TYPES_TABLE_NAME
from source.database.instance import db
from source.database.seeders.xp_event_type import seed_xp_event_type


@click.command("seed-db")
def seed_db():
    """Seed database.

    Raises
    ------
    SQLAlchemyError
    """
    try:
        click.echo(f"Database: Seeding {XP_EVENT_TYPES_TABLE_NAME} table.")
        seed_xp_event_type(db.session)
        click.echo(f"Database: {XP_EVENT_TYPES_TABLE_NAME} table seeded successfully!")

    except SQLAlchemyError as error:
        logging.error(f"(LOG): Error seeding table {XP_EVENT_TYPES_TABLE_NAME}: {error}")
