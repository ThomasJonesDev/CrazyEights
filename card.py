import pygame.image

import suits
from filepath import FilePath


class Card:

    def __init__(self, card_value: int, card_suit: suits.Suits) -> None:
        image_file_path: str = FilePath.get_file_path('images\\Playing Cards\\')
        self.card_value: int = card_value
        self.card_suit: suits.Suits = card_suit
        self.card_image: pygame.surface.Surface = pygame.image.load(
            image_file_path + 'card-' + self.card_suit.value + '-' + str(self.card_value) + '.png')

    def get_card_value(self) -> int:
        return self.card_value

    def get_card_suit(self) -> suits.Suits:
        return self.card_suit

    def get_card_image(self) -> pygame.surface.Surface:
        return self.card_image

    @staticmethod
    def get_face_card_value(value: chr) -> int | None:
        if value == 'J':
            return 11
        elif value == 'Q':
            return 12
        elif value == 'K':
            return 13
