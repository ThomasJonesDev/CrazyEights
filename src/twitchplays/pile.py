from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .card import Card


class Pile:

    def __init__(self) -> None:
        self._pile: list["Card"] = []

    def add_to_pile(self, card_to_add: "Card") -> None:
        self._pile.append(card_to_add)

    def get_top_card(self) -> "Card":
        return self._pile[-1]

    def get_pile(self) -> list["Card"]:
        return self._pile
    
    def reset_pile(self) -> None:
        self._pile = []
