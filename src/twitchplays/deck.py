import random

from .card import Card
from .suits import Suits


class Deck:
    """An instance of the Deck, with useful functions"""

    def __init__(self) -> None:
        """Creates the Deck, and shuffles it"""
        self._deck: list["Card"] = self._create_deck()
        self.shuffle_deck()

    @staticmethod
    def _create_deck() -> list["Card"]:
        """Add all 52 cards to the deck

        Returns:
            list[Card]: deck list with all 52 playing cards
        """
        _deck: list["Card"] = []
        for suit in Suits:
            for value in range(1, 14):
                _deck.append(Card(value, suit))
        return _deck

    def shuffle_deck(self) -> None:
        """randomly shuffles the deck"""
        random.shuffle(self._deck)

    def draw_card(self) -> "Card":
        """draw a card from the top of the deck

        Returns:
            Card: card object drawn from deck
        """
        return self._deck.pop()

    def get_deck(self) -> list["Card"]:
        """Gets the entire Deck

        Returns:
            List[Card]: returns the entire list of card objects
        """
        return self._deck

    def get_num_of_cards_in_deck(self) -> int:
        """Gets how many cards are remaining in the deck

        Returns:
            int: number of cards in the deck
        """
        return len(self._deck)

    def add_to_deck(self, cards: list["Card"]) -> None:
        """Adds card objects to the deck (replenish deck when empty)

        Args:
            cards (list[Card]): List of card objects to add to deck
        """
        for card in cards:
            self._deck.append(card)
