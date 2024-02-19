from unittest import TestCase
from crazyeights import CrazyEights
from player import Player
from card import Card
from suits import Suits


class TestCrazyEights(TestCase):
    def test_get_select_card(self):
        player = Player()
        card = Card(13, Suits.SPADES)
        hand = [card]
        player.add_card_to_hand(card)
        self.assertEqual((13, 'S'), CrazyEights.get_select_card((14, 'S'), hand))
