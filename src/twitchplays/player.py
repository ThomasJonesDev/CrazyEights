from typing import TYPE_CHECKING

from .suits import Suits

if TYPE_CHECKING:
    from .card import Card


class Player:
    """A instance of a player. Contains players hand and useful functions
    """

    def __init__(self) -> None
        """Initialise the players hand
        """
        self._player_hand: list["Card"] = []

    def get_hand(self) -> list["Card"]:
        """Gets the hand (cards) that the player has

        Returns:
            list[Card]: a list of cards that the player has
        """
        return self._player_hand

    def get_num_of_cards(self) -> int:
        """Counts how many cards the player has in their hand

        Returns:
            int: an integer value of how many cards the player has
        """
        return len(self._player_hand)

    def add_card(self, card: "Card") -> None:
        """Adds a card to a players hand

        Args:
            card (Card): The object of the card to add to hand
        """
        self._player_hand.append(card)

    def remove_card(self, card: "Card") -> "Card":
        """Removes a card from the players hand

        Args:
            card (Card): The object of the card to remove from the players hand

        Returns:
            Card: The object of the card that was removed from the players hand
        """
        self._player_hand.remove(card)
        return card

    def get_card(self, card: tuple[int, str]) -> "Card | None":
        """Takes in a tuple representing a card, and returns the card object if it is in the players hand

        Args:
            card (tuple[int, str]): tuple representing a card (value, suit)

        Returns:
            Card | None: The object of the card if player has it, otherwise return None
        """
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
