from typing import TYPE_CHECKING

from .suits import Suits

if TYPE_CHECKING:
    from .card import Card


class Player:

    def __init__(self) -> None:
        self._player_hand: list["Card"] = []

    def get_hand(self) -> list["Card"]:
        return self._player_hand

    def get_num_of_cards(self) -> int:
        return len(self._player_hand)

    def add_card(self, card: "Card") -> None:
        self._player_hand.append(card)

    def remove_card(self, card: "Card") -> "Card":
        self._player_hand.remove(card)
        return card

    def get_card(self, card: tuple[int, str]) -> "Card | None":
        for player_card in self.get_hand():
            if card[0] == player_card.get_card_value():
                if card[1] == "C" and player_card.get_card_suit() is Suits.CLUBS:
                    return player_card
                if card[1] == "D" and player_card.get_card_suit() is Suits.DIAMONDS:
                    return player_card
                if card[1] == "H" and player_card.get_card_suit() is Suits.HEARTS:
                    return player_card
                if card[1] == "S" and player_card.get_card_suit() is Suits.SPADES:
                    return player_card
        return None
