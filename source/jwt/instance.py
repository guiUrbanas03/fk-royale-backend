"""Instantiate the jwt wrapper."""
from flask_jwt_extended import JWTManager

jwt: JWTManager = JWTManager()
