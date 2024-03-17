import unittest

from src.twitchplays.card import Card
from src.twitchplays.crazyeights import CrazyEights
from src.twitchplays.player import Player
from src.twitchplays.suits import Suits


class TestCrazyEights(unittest.TestCase):
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
        print(self.assertEqual((13, "S"), CrazyEights.get_select_card((14, "S"), hand)))


if __name__ == "__main__":
    unittest.main()
