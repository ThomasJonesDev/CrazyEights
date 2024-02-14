import pygame.image


class Card:

    def __init__(self, card_value, card_suit):
        self.card_value = card_value
        self.card_suit = card_suit
        self.card_image = pygame.image.load('images/Playing Cards/card-'
                                            + self.card_suit.lower()
                                            + '-'
                                            + card_value
                                            + '.png')

    def get_card_value(self):
        return self.card_value

    def get_card_suit(self):
        return self.card_suit

    def get_card_image(self):
        return self.card_image

