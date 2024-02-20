from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from card import Card


class Player:

    def __init__(self) -> None:
        self._player_hand: list['Card'] = []

    def get_player_hand(self) -> list['Card']:
        return self._player_hand

    def get_how_many_cards_player_has(self) -> int:
        return len(self._player_hand)

    def add_card_to_hand(self, card: 'Card') -> None:
        self._player_hand.append(card)

    def play_card(self, card: 'Card') -> 'Card':
        self._player_hand.remove(card)
        return card
