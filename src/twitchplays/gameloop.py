import os
import time

import pygame

from .ai_agent import AiAgent
from .card import Card
from .countdown import Countdown
from .crazyeights import CrazyEights
from .currentplayer import CurrentPlayer
from .deck import Deck
from .gamerender import GameRenderer
from .pile import Pile
from .player import Player
from .twitch_crowdsourcing import TwitchCrowdsourcing

FPS = 1
NUMBER_OF_STARTING_CARDS = 7


class GameLoop:
    """Where the program and game loop runs"""

    def __init__(self) -> None:
        """Initiate instances and global variables"""
        pygame.init()
        self._clock = pygame.time.Clock()
        self._renderer = GameRenderer()
        self._tcs = TwitchCrowdsourcing()
        self._countdown = Countdown()

        self._chat = None
        self._ai = None
        self._deck = None
        self._pile = None
        self._ai_agent = None
        self._game_state = None

        self.prog_loop()

    def prog_loop(self) -> None:
        """
        The program loop, allows for another game to be run after finishing a game
        Can also process user inputs
        """
        while True:
            self._renderer.render_message("Press ENTER to play")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close_program()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.init_new_game()
                        self.game_loop()

    def game_loop(self) -> None:
        """
        The game loop
        Can process user inputs
        """
        while True:
            # Render the game
            self._render_game()
            # Process Mouse/Keyboard Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close_program()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            if self._game_state == CurrentPlayer.TWITCH_PLAYING:
                self.twitch__chat_move()
                if self._check_win_conditions(self._chat):
                    self._renderer.render_message("Twitch Chat won!")
                    time.sleep(3)
                    return
            elif self._game_state == CurrentPlayer.AI_PLAYING:
                self._ai_move()
                if self._check_win_conditions(self._ai):
                    self._renderer.render_message("The AI won!")
                    time.sleep(3)
                    return

            self._clock.tick(FPS)

    def close_program(self) -> None:
        """Shuts down the twitch IRC connection then close program & threads"""
        self._tcs.diconnect()
        os._exit(0)  # used to close listening thread

    def init_new_game(self) -> None:
        """Initialise variables to set up a new game, and deal out starting cards"""
        # Global Vars
        self._countdown = Countdown()
        self._chat = Player()
        self._ai = Player()
        self._deck = Deck()
        self._pile = Pile()
        self._ai_agent = AiAgent()
        # Deal out starting cards
        for _ in range(NUMBER_OF_STARTING_CARDS):
            self._chat.add_card(self._deck.draw_card())
            self._ai.add_card(self._deck.draw_card())
        # Put first card onto the _pile
        self._pile.add_to_pile(self._deck.draw_card())
        # Start game state in player ones(_chat) go.
        self._game_state = CurrentPlayer.TWITCH_PLAYING

    def _ai_move(self) -> None:
        """PLACEHOLDER FUNCTION, finds first playable card in AI hand and plays it"""
        self._pick_up_card(self._ai)
        for card in self._ai.get_hand():
            if CrazyEights.can_card_be_played(card, self._pile.get_top_card()):
                self._pile.add_to_pile(self._ai.remove_card(card))
                break
        self._game_state = CurrentPlayer.TWITCH_PLAYING
        return

    def twitch__chat_move(self) -> None:
        """
        If player doesn't have any cards they can play, pick up cards.
        Then get the choosen card from Twitch and play it
        """
        # If player doesnt have any valid moves keep picking up cards
        self._pick_up_card(self._chat)

        if self._countdown.is_countdown_running() is False:
            self._countdown.start_countdown()
            self._tcs.start_collecting_answers()

        if (
            self._countdown.is_countdown_running()
            and self._countdown.get_seconds_remaining() > 0
        ):
            self._renderer.render_time_remaining(
                self._countdown.get_seconds_remaining()
            )

        # If 30 second _countdown has ended
        if (
            self._countdown.is_countdown_running() is True
            and self._countdown.get_seconds_remaining() <= 0
        ):
            self._countdown.stop_countdown()
            card: Card = self._get_twitch_choice()
            self._pile.add_to_pile(self._chat.remove_card(card))
            self._game_state = CurrentPlayer.AI_PLAYING

    def _pick_up_card(self, player: Player) -> None:
        """Pick up cards until player has a playable card

        Args:
            player (Player): player object, to add card to
        """
        while (
            CrazyEights.can_player_play_a_card(
                player.get_hand(), self._pile.get_top_card()
            )
            is False
        ):
            self._player_draw_card(player)
            time.sleep(1)  # Delay so each card card being picked us is seen

    def _get_twitch_choice(self) -> Card:
        """
        Use TwitchCrowdsourcing to get a list of cards
        Go through list to find if any choosen cards can be played
        If there is no card in the list that can be played go through Twitch hand and find first card that can be played

        Returns:
            Card: card object to be played
        """
        tcs_answers: list[tuple[int, str]] = self._tcs.get_submitted_answers()
        if len(tcs_answers) > 0:
            tcs_answer = tcs_answers[0]
        else:
            return self._get_random_card_to_play()

        for tcs_answer in tcs_answers:
            # conver card var to Card
            card: Card | None = self._chat.get_card(tcs_answer)
            if card is not None:
                if CrazyEights.can_card_be_played(card, self._pile.get_top_card()):
                    return card
        return self._get_random_card_to_play()

    def _get_random_card_to_play(self) -> Card:
        """Loop through cards in Twitch hand until coming accross a card that can be played

        Returns:
            Card: card object that can be played
        """
        _chats_hand = self._chat.get_hand()
        for card in _chats_hand:
            if CrazyEights.can_card_be_played(card, self._pile.get_top_card()) is True:
                return card
        # Will never be reached, stop Not all path ret a value err
        return _chats_hand[0]

    def _player_draw_card(self, player: Player) -> None:
        """
        Player takes a card from the top of the deck
        If player takes the last card from the deck, replenish deck from pile and shuffle

        Args:
            player (Player): player object of player drawing a card
        """
        player.add_card(self._deck.draw_card())
        deck_size = self._deck.get_num_of_cards_in_deck()
        if deck_size == 0:
            _pile = self._pile.get_pile()
            pile_top_card = _pile.pop()
            self._pile.empty_pile()
            self._pile.add_to_pile(pile_top_card)
            self._deck.add_to_deck(_pile)
            self._deck.shuffle_deck()
        self._render_game()

    def _check_win_conditions(self, player: Player) -> bool:
        """Checks if player has no cards in their hand

        Args:
            player (Player): player object to check hand

        Returns:
            bool: if the player has won, by having no cards in hand. True for won, False not not won.
        """
        if player.get_num_of_cards() == 0:
            return True
        return False

    def _render_game(self) -> None:
        """function that calls for game to be rerendered"""
        self._renderer.render(self._deck, self._pile, self._chat, self._ai)
