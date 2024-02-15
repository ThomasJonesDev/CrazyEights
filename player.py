class Player:

    def __init__(self):
        self.player_hand = []

    def get_player_hand(self):
        return self.player_hand

    def get_card_from_deck(self, card):
        self.player_hand.append(card)

    def play_card(self, card):
        return self.player_hand.pop(card)
