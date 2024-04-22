from enum import Enum


class CurrentPlayer(Enum):
    """Enum to represent which player turn it currently is

    Args:
        Enum (_type_): _description_
    """

    AI_PLAYING = 0
    TWITCH_PLAYING = 1
