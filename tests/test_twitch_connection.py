import unittest

from src.twitchconnection import TwitchConnection


class TestTwitchConnection(unittest.TestCase):
    """
    Test class that initialises TwitchConnection for manual testing
    """

    def manual_testing(self):
        x = TwitchConnection()
        print(x)
