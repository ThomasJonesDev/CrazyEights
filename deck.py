import random
from suits import Suits
from card import Card


class Deck:

    def __init__(self):
        self.deck = self.create_deck(self)
        self.shuffle_deck(self)

    @staticmethod
    def _create_deck(self):
        deck = []
        for suit in Suits:
            for value in range(1, 14):
                deck.append(Card(suit, value))
        return deck

    @staticmethod
    def _shuffle_deck(self):
        random.shuffle(self.deck)

    def draw_card(self):
        return self.deck.pop()
