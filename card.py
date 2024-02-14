class Card:

    def __int__(self, card_value, card_suit, card_image):
        self.card_value = card_value
        self.card_suit = card_suit
        self.card_image = card_image

    def get_card_value(self):
        return self.card_value

    def get_card_suit(self):
        return self.card_suit

    def get_card_image(self):
        return self.card_image

