from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from card import Card
    from pile import Pile


class CrazyEights:

    @staticmethod
    def is_valid_move(selected_card: 'Card', top_of_pile: 'Card') -> bool:
        # Crazy Eights the 8 can always be played
        if selected_card.get_card_value() == 8:
            return True
        # Otherwise check if either the suit of the number of the card matches the card on the pile
        elif (selected_card.get_card_value() == top_of_pile.get_card_value()
                or selected_card.get_card_suit() == top_of_pile.get_card_suit()):
            return True
        return False

    @staticmethod
    def get_select_card(selected_card: tuple[int, chr], players_hand: list['Card']) -> 'Card':
        selected_card_value: int = selected_card[0]
        selected_card_suit: chr = selected_card[1].upper()
        # Loop through each card, and returns the card that matches the value and suit
        for card in players_hand:
            if card.get_card_value() == selected_card_value:
                # get first letter and convert to upper as get_card_suit returns lowercase string of suit name
                if card.get_card_suit().value[0].upper() == selected_card_suit:
                    return card

    @staticmethod
    def check_if_any_valid_moves(player_hand: list['Card'], top_of_pile: 'Card') -> bool:
        for card in player_hand:
            if CrazyEights.is_valid_move(card, top_of_pile):
                return True
        return False

    @staticmethod
    def calculate_players_score(players_hand: list['Card']) -> int:
        score: int = 0
        for card in players_hand:
            card_value: int = card.get_card_value()
            if 10 <= card_value <= 13:
                score += 10
            elif card_value == 8:
                score += 50
            else:
                score += card_value
            return score
