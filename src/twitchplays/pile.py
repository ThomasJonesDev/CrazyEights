from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .card import Card


class Pile:
    """An instance of the Pile, with useful functions"""

    def __init__(self) -> None:
        """Creates the pile"""
        self._pile: list["Card"] = []

    def add_to_pile(self, card_to_add: "Card") -> None:
        """Adds a card object to the pile

        Args:
            card_to_add (Card): card object to add
        """
        self._pile.append(card_to_add)

    def get_top_card(self) -> "Card":
        """Gets the card object that is on top of the pile (last in list)

        Returns:
            Card: card object
        """
        return self._pile[-1]

    def get_pile(self) -> list["Card"]:
        """Gets the entire pile

        Returns:
            List[Card]: returns the entire list of card objects
        """
        return self._pile

    def empty_pile(self) -> None:
        """Sets the pile to a empty list, is used for when deck is empty and cards in pile
        (except from the top one) are taken from the pile to be put back into the deck
        """
        self._pile = []
