"""Instantiate the database wrapper."""
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
