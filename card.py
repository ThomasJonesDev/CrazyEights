from typing import TYPE_CHECKING

from pygame import image

from filepath import FilePath

if TYPE_CHECKING:
    from pygame import Surface

    from suits import Suits


class Card:

    def __init__(self, card_value: int, card_suit: "Suits") -> None:
        self._card_value: int = card_value
        self._card_suit: Suits = card_suit
        image_file_path: str = FilePath.get_file_path("images/Playing Cards/")
        self._card_image: Surface = image.load(
            image_file_path
            + "card-"
            + self._card_suit.value
            + "-"
            + str(self._card_value)
            + ".png"
        )

    def get_card_value(self) -> int:
        return self._card_value

    def get_card_suit(self) -> "Suits":
        return self._card_suit

    def get_card_image(self) -> "Surface":
        return self._card_image

    @staticmethod
    def get_face_card_value(value: str) -> int:
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
