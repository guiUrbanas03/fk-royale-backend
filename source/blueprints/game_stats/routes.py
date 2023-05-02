"""Handle game_stats requests."""
from flask import Blueprint, jsonify

from source.constants.blueprints import GAME_STATS_BLUEPRINT_NAME

game_stats_bp = Blueprint(
    GAME_STATS_BLUEPRINT_NAME, __name__, url_prefix=f"/{GAME_STATS_BLUEPRINT_NAME}"
)


@game_stats_bp.route("/")
def game_stats_index():
    """Index request."""
    return jsonify({"data": "Game stats"})
