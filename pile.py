from card import Card


class Pile:

    def __init__(self):
        self.pile = []

    def add_to_pile(self, card):
        self.pile.append(card)

    def show_top_card(self):
        return self.pile[-1]
