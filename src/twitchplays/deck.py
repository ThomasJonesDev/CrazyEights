import random

from .card import Card
from .suits import Suits


class Deck:
    """_summary_"""

    def __init__(self) -> None:
        """_summary_"""
        self._deck: list["Card"] = self._create_deck()
        self._shuffle_deck()

    @staticmethod
    def _create_deck() -> list["Card"]:
        """_summary_

        Returns:
            _type_: _description_
        """
        _deck: list["Card"] = []
        for suit in Suits:
            for value in range(1, 14):
                _deck.append(Card(value, suit))
        return _deck

    def _shuffle_deck(self) -> None:
        """_summary_"""
        random.shuffle(self._deck)

    def draw_card(self) -> "Card":
        """_summary_

        Returns:
            Card: _description_
        """
        return self._deck.pop()

    def get_deck(self) -> list["Card"]:
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._deck

    def get_num_of_cards_in_deck(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return len(self._deck)

    def add_to_deck(self, cards: list["Card"]) -> None:
        """_summary_

        Args:
            cards (list[&quot;Card&quot;]): _description_
        """
        for card in cards:
            self._deck.append(card)
