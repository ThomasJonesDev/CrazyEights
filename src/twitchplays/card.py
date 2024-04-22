from typing import TYPE_CHECKING

from pygame import image

if TYPE_CHECKING:
    from pygame import Surface

    from .suits import Suits


class Card:
    """An instance of a playing card"""

    def __init__(self, card_value: int, card_suit: "Suits") -> None:
        """Initialise a instance of a playing card

        Args:
            card_value (int): e.g. 13 (King)
            card_suit (Suits): e.g. Suits.SPADE
        """
        self._card_value: int = card_value
        self._card_suit: Suits = card_suit
        _image_file_path: str = "./src/images/cards/"
        self._card_image: Surface = image.load(
            _image_file_path
            + "card-"
            + self._card_suit.value
            + "-"
            + str(self._card_value)
            + ".png"
        )

    def get_card_value(self) -> int:
        """Gets the playing cards value

        Returns:
            int: e.g. 13 (King)
        """
        return self._card_value

    def get_card_suit(self) -> "Suits":
        """Gets the playing cards suit

        Returns:
            Suits: e.g. Suits.SPADE
        """
        return self._card_suit

    def get_card_image(self) -> "Surface":
        """Gets the image of the front of the playing card

        Returns:
            Surface: image of playing card
        """
        return self._card_image

    @staticmethod
    def get_court_card_value(value: str) -> int:
        """For the court cards (Jack, Queen, King, Ace) return the value

        Args:
            value (str): e.g. A

        Returns:
            int: e.g. 1
        """
        value = value.upper()
        if value == "A":
            return 1
        elif value == "J":
            return 11
        elif value == "Q":
            return 12
        elif value == "K":
            return 13
        return int(value)
