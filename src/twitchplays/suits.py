from enum import Enum


class Suits(Enum):
    """Enums to represent a playing cards suit

    Args:
        Enum (string): string of the suit
    """

    CLUBS: str = "clubs"
    DIAMONDS: str = "diamonds"
    HEARTS: str = "hearts"
    SPADES: str = "spades"
