import random

from .card import Card
from .suits import Suits


class Deck:

    def __init__(self) -> None:
        self._deck: list["Card"] = self._create_deck()
        self._shuffle_deck()

    @staticmethod
    def _create_deck() -> list["Card"]:
        _deck: list["Card"] = []
        for suit in Suits:
            for value in range(1, 14):
                _deck.append(Card(value, suit))
        return _deck

    def _shuffle_deck(self) -> None:
        random.shuffle(self._deck)

    def draw_card(self) -> "Card":
        return self._deck.pop()

    def get_deck(self) -> list["Card"]:
        return self._deck

    def get_num_of_cards_in_deck(self) -> int:
        return len(self._deck)

    def add_to_deck(self, cards: list["Card"]) -> None:
        for card in cards:
            self._deck.append(card)
