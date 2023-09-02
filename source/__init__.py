"""App factory."""
import os
from flask import Flask
from flask.logging import create_logger
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from source.blueprints.auth.routes import auth_bp
from source.blueprints.game_stats.routes import game_stats_bp
from source.blueprints.index.routes import index_bp
from source.blueprints.profile.routes import profile_bp
from source.blueprints.report.routes import report_bp
from source.blueprints.user.routes import user_bp
from source.blueprints.xp_event_type.routes import xp_event_type_bp
from source.commands.seeders import seed_db
from source.database.instance import db
from source.errors.json_error import build_error_response
from source.jwt.instance import jwt
from source.socketio.instance import socketio


def create_app(test_config=None) -> Flask:
    """Create a flask App."""
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, origins=["*"])

    app.config.from_object("config.settings")
    app.config.from_prefixed_env()

    if test_config is None:
        app.config.from_pyfile("env.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    create_logger(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_error_handlers(app)

    return app


def register_extensions(app: Flask):
    """Register app extensions."""
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")


def register_blueprints(app: Flask):
    """Register app blueprints."""
    app.register_blueprint(index_bp)
    app.register_blueprint(game_stats_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(xp_event_type_bp)
    app.register_blueprint(auth_bp)


def register_commands(app: Flask):
    """Register app commands."""
    app.cli.add_command(seed_db)


def register_error_handlers(app: Flask):
    """Register all app error handlers."""
    app.register_error_handler(HTTPException, build_error_response)
    app.register_error_handler(Exception, build_error_response)


def add_header():
    """Add headers to app requests."""
