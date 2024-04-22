from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .card import Card


class CrazyEights:
    """_summary_

    Returns:
        _type_: _description_
    """

    @staticmethod
    def can_card_be_played(selected_card: "Card", top_of_pile: "Card") -> bool:
        """_summary_

        Args:
            selected_card (Card): _description_
            top_of_pile (Card): _description_

        Returns:
            bool: _description_
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
        """_summary_

        Args:
            selected_card (tuple[int, str]): _description_
            players_hand (list[&quot;Card&quot;]): _description_

        Returns:
            Card | None: _description_
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
        """_summary_

        Args:
            player_hand (list[&quot;Card&quot;]): _description_
            top_of_pile (Card): _description_

        Returns:
            bool: _description_
        """
        for card in player_hand:
            if CrazyEights.can_card_be_played(card, top_of_pile):
                return True
        return False

    @staticmethod
    def calculate_player_score(players_hand: list["Card"]) -> int:
        """_summary_

        Args:
            players_hand (list[&quot;Card&quot;]): _description_

        Returns:
            int: _description_
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
