import random

from .card import Card
from .suits import Suits


class Deck:

    def __init__(self) -> None:
        self.deck: list["Card"] = self._create_deck()
        self._shuffle_deck()

    @staticmethod
    def _create_deck() -> list["Card"]:
        deck: list["Card"] = []
        for suit in Suits:
            for value in range(1, 14):
                deck.append(Card(value, suit))
        return deck

    def _shuffle_deck(self) -> None:
        random.shuffle(self.deck)

    def draw_card(self) -> "Card":
        return self.deck.pop()

    def get_deck(self) -> list["Card"]:
        return self.deck
