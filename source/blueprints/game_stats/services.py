from uuid import uuid4

from source.dtos.game_stats import CreateGameStatsDTO
from source.models.game_stats.game_stats import GameStats


def create_new_game_stats(session, game_stats_data: CreateGameStatsDTO) -> GameStats:
    """Create new game stats.

    Parameters
    ----------
    game_stats_data: CreateGameStatsDTO

    Returns
    -------
    GameStats
    """
    game_stats = GameStats(**game_stats_data, id=uuid4())

    session.add(game_stats)
    session.flush()

    return game_stats
