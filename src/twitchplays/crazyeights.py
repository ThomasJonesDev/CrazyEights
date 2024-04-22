from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .card import Card


class CrazyEights:
    """class of static functions to check game rules"""

    @staticmethod
    def can_card_be_played(selected_card: "Card", top_of_pile: "Card") -> bool:
        """Checks a card with the card on top of the pile, to see if it can be played (put onto the top of the pile)

        Args:
            selected_card (Card): card to check
            top_of_pile (Card): card on the top of the pile

        Returns:
            bool: return True if card can be played, else returns Flase
        """
        # Crazy Eights the 8 can always be played
        if selected_card.get_card_value() == 8:
            return True
        # Otherwise check if either the suit of the number of the card matches the card on the pile
        elif (
            selected_card.get_card_value() == top_of_pile.get_card_value()
            or selected_card.get_card_suit() == top_of_pile.get_card_suit()
        ):
            return True
        return False

    @staticmethod
    def get_card(
        selected_card: tuple[int, str], players_hand: list["Card"]
    ) -> "Card | None":
        """Gets the card object from a players hand, that matches the card represented by a tuple

        Args:
            selected_card (tuple[int, str]): Card represented as a tuple e.g. (5, D)
            players_hand (list[Card]): list of card object in hand

        Returns:
            Card | None: If card object is in hand return object, else return None
        """
        selected_card_value: int = selected_card[0]
        selected_card_suit: str = selected_card[1].upper()
        # Loop through each card, and returns the card that matches the value and suit
        for card in players_hand:
            if card.get_card_value() == selected_card_value:
                # get first letter and convert to upper as get_card_suit returns lowercase string of suit name
                if card.get_card_suit().value[0].upper() == selected_card_suit:
                    return card
        return None

    @staticmethod
    def can_player_play_a_card(player_hand: list["Card"], top_of_pile: "Card") -> bool:
        """Checks all the cards in a players hand to see if any of them can be played

        Args:
            player_hand (list[Card]): list of cards in players hand
            top_of_pile (Card): card that is on the top of the pile

        Returns:
            bool: True if there is a card that can be played, otherwiser return false
        """
        for card in player_hand:
            if CrazyEights.can_card_be_played(card, top_of_pile):
                return True
        return False

    @staticmethod
    def calculate_player_score(players_hand: list["Card"]) -> int:
        """calculates a score based on what cards are in a players hand

        Args:
            players_hand (list[Card]): list of cards in hand

        Returns:
            int: score
        """
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
