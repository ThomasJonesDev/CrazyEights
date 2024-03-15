from unittest import TestCase

from src.card import Card
from src.crazyeights import CrazyEights
from src.player import Player
from src.suits import Suits


class TestCrazyEights(TestCase):
    def test_is_valid_move(self):
        card1 = Card(1, Suits.CLUBS)
        card2 = Card(13, Suits.CLUBS)
        self.assertTrue(CrazyEights.is_valid_move(card1, card1))
        self.assertFalse(CrazyEights.is_valid_move(card1, card2))

    def test_get_select_card(self):
        player = Player()
        card = Card(13, Suits.SPADES)
        hand = [card]
        player.add_card_to_hand(card)
        self.assertEqual((13, "S"), CrazyEights.get_select_card((14, "S"), hand))
