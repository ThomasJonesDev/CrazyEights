import unittest
from unittest.case import TestCase

from src.twitchplays.twitch_crowdsourcing import TwitchCrowdsourcing
from src.twitchplays.twitchconnection import TwitchConnection

card_dict: dict[str, int] = {
    "AS": 0,
    "2S": 0,
    "3S": 0,
    "4S": 0,
    "5S": 0,
    "6S": 0,
    "7S": 0,
    "8S": 0,
    "9S": 0,
    "10S": 0,
    "JS": 0,
    "QS": 0,
    "KS": 0,
    "AC": 0,
    "2C": 0,
    "3C": 0,
    "4C": 0,
    "5C": 0,
    "6C": 0,
    "7C": 0,
    "8C": 0,
    "9C": 0,
    "10C": 0,
    "JC": 0,
    "QC": 0,
    "KC": 0,
    "AH": 0,
    "2H": 0,
    "3H": 0,
    "4H": 0,
    "5H": 0,
    "6H": 0,
    "7H": 0,
    "8H": 0,
    "9H": 0,
    "10H": 0,
    "JH": 0,
    "QH": 0,
    "KH": 0,
    "AD": 0,
    "2D": 0,
    "3D": 0,
    "4D": 0,
    "5D": 0,
    "6D": 0,
    "7D": 0,
    "8D": 0,
    "9D": 0,
    "10D": 0,
    "JD": 0,
    "QD": 0,
    "KD": 0,
}


class TestTwitchCrowdsourcing(unittest.TestCase):

    def test_convert_card_str_to_tuple(self):
        input: list[str] = ["10H", "4C"]
        output: list[tuple[int, str]] = [(10, "H"), (4, "C")]
        self.assertEqual(output, TwitchCrowdsourcing._convert_card_str_to_tuple(input))

    def test_get_list_of_choosen_card(self):
        input_dict: dict[str, str] = {
            "player1": "AS",
            "player2": "AC",
            "player3": "AS",
            "player4": "10S",
        }

        output_list: list[str] = ["AS", "AC", "10S"]

        self.assertEqual(
            output_list, TwitchCrowdsourcing._get_list_of_choosen_cards(input_dict)
        )

    def test_create_card_tally(self):
        dictionary: dict[str, int] = {
            "AS": 0,
            "2S": 0,
            "3S": 0,
            "4S": 0,
            "5S": 0,
            "6S": 0,
            "7S": 0,
            "8S": 0,
            "9S": 0,
            "10S": 0,
            "JS": 0,
            "QS": 0,
            "KS": 0,
            "AC": 0,
            "2C": 0,
            "3C": 0,
            "4C": 0,
            "5C": 0,
            "6C": 0,
            "7C": 0,
            "8C": 0,
            "9C": 0,
            "10C": 0,
            "JC": 0,
            "QC": 0,
            "KC": 0,
            "AH": 0,
            "2H": 0,
            "3H": 0,
            "4H": 0,
            "5H": 0,
            "6H": 0,
            "7H": 0,
            "8H": 0,
            "9H": 0,
            "10H": 0,
            "JH": 0,
            "QH": 0,
            "KH": 0,
            "AD": 0,
            "2D": 0,
            "3D": 0,
            "4D": 0,
            "5D": 0,
            "6D": 0,
            "7D": 0,
            "8D": 0,
            "9D": 0,
            "10D": 0,
            "JD": 0,
            "QD": 0,
            "KD": 0,
        }

        self.assertEqual(dictionary, TwitchCrowdsourcing._create_card_tally())

    def test_parse_input(self):
        input: list[str] = [":foo!foo@foo.tmi.twitch.tv PRIVMSG #bar :bleedPurple"]
        self.assertEqual(
            {"foo": "bleedPurple"}, TwitchCrowdsourcing._parse_input(input)
        )

    def test_filter_answers(self):
        dictionary = {
            "player1": "  ",
            "player2": "1S",
            "player3": "7S",
            "player4": "fjasdlgjklgj",
        }
        self.assertEqual(
            {"player3": "7S"}, TwitchCrowdsourcing._filter_answers(dictionary)
        )


if __name__ == "__main__":
    unittest.main()
