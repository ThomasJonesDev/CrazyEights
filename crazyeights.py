from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from card import Card


class CrazyEights:

    @staticmethod
    def is_valid_move(selected_card: 'Card', top_of_pile: 'Card') -> bool:
        if selected_card.get_card_value() != top_of_pile.get_card_value():
            if selected_card.get_card_suit() != top_of_pile.get_card_suit():
                return False
        return True

    @staticmethod
    def get_select_card(selected_card: tuple[int, chr], players_hand: list['Card']) -> 'Card':
        selected_card_value: int = selected_card[0]
        selected_card_suit: chr = selected_card[1]
        # Loop through each card, and returns the card that matches the value and suit
        for card in players_hand:
            if card.get_card_value() == selected_card_value:
                if card.get_card_suit().value[0].upper() == selected_card_suit:
                    return card
