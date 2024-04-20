import pygame
import os
import time

from .card import Card
from .countdown import Countdown
from .crazyeights import CrazyEights
from .deck import Deck
from .gamerender import GameRenderer
from .gamestate import GameState
from .pile import Pile
from .player import Player
from .twitch_crowdsourcing import TwitchCrowdsourcing
from .ai_agent import AiAgent

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
GAME_TITLE = "Twitch Plays"
FPS = 1
BACKGROUND_COLOUR = [0, 255, 0]
BACK_OF_CARD = pygame.image.load("src/images/cards/card-back1.png")
NUMBER_OF_STARTING_CARDS = 7


class GameLoop:

    def __init__(self) -> None:
        # Init classes and global variables
        pygame.init()
        self.clock = pygame.time.Clock()
        self.renderer = GameRenderer()
        self.tcs = TwitchCrowdsourcing()
        self.prog_loop()

    def prog_loop(self) -> None:
        while True:
            self.renderer.render_message("Press ENTER to play")
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.close_program()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.init_new_game()
                            self.game_loop()


    def game_loop(self) -> None:
        while True:
            # Render the game
            self.redraw_game()
            # Process Mouse/Keyboard Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close_program()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            if self.game_state == GameState.TWITCH_PLAYING:
                self.twitch_chat_move()
                if self.has_player_won(self.chat):
                    self.renderer.render_message("Twitch Chat won!")
                    time.sleep(3)
                    return
            elif self.game_state == GameState.AI_PLAYING:
                self.ai_move()
                if self.has_player_won(self.ai):
                    self.renderer.render_message("The AI won!")
                    time.sleep(3)
                    return
            else:
                raise Exception

            self.clock.tick(FPS)

    def close_program(self) -> None:
        self.tcs.diconnect()
        os._exit(0) # used to close listening thread

    def init_new_game(self) -> None:
        # Global Vars
        self.countdown = Countdown()
        self.chat = Player()
        self.ai = Player()
        self.deck = Deck()
        self.pile = Pile()
        self.ai_agent = AiAgent()
        # Deal out starting cards
        for _ in range(NUMBER_OF_STARTING_CARDS):
            self.chat.add_card_to_hand(self.deck.draw_card())
            self.ai.add_card_to_hand(self.deck.draw_card())
        # Put first card onto the pile
        self.pile.add_to_pile(self.deck.draw_card())
        # Start game state in player ones(chat) go.
        self.game_state = GameState.TWITCH_PLAYING

    def ai_move(self) -> None:
        # PLACE HOLDER FUNCTION
        self.pick_up_card(self.ai)
        for card in self.ai.get_player_hand():
            if CrazyEights.check_if_valid_move(card, self.pile.get_top_card()):
                break  
        self.pile.add_to_pile(self.ai.play_card(card))
        self.game_state = GameState.TWITCH_PLAYING
        return

    def twitch_chat_move(self) -> None:
        # If player doesnt have any valid moves keep picking up cards
        self.pick_up_card(self.chat)

        if self.countdown.is_countdown_running() is False:
            self.countdown.start_countdown()
            self.tcs.start_collecting_answers()

        if self.countdown.is_countdown_running() and self.countdown.get_countdown_in_seconds() > 0:
            self.renderer.render_time_remaining(self.countdown.get_countdown_in_seconds())

        # If 30 second countdown has ended
        if self.countdown.is_countdown_running() is True and self.countdown.get_countdown_in_seconds() <= 0:
            self.countdown.stop_countdown()
            card: Card = self.get_valid_move_from_chat()
            self.pile.add_to_pile(self.chat.play_card(card))
            self.game_state = GameState.AI_PLAYING

    def pick_up_card(self, player: Player) -> None:
        while CrazyEights.check_if_any_valid_moves(player.get_player_hand(), self.pile.get_top_card()) is False:
            time.sleep(1)
            self.player_draw_card(player)

    def get_valid_move_from_chat(self) -> Card:
        tcs_answers: list[tuple[int, str]] = self.tcs.get_submitted_answers()
        if len(tcs_answers) > 0:
            tcs_answer = tcs_answers[0]
        else:
            return self.select_random_card()

        for tcs_answer in tcs_answers:
            # conver card var to Card
            card: Card | None = self.chat.get_card(tcs_answer)
            if card is not None:
                if CrazyEights.check_if_valid_move(card, self.pile.get_top_card()):
                    return card
        return self.select_random_card()

    def select_random_card(self) -> Card:
        chats_hand = self.chat.get_player_hand()
        for card in chats_hand:
            if CrazyEights.check_if_valid_move(card, self.pile.get_top_card()) is True:
                return card
        return chats_hand[0]  # Will never be reached, stop Not all path ret a value err

    def player_draw_card(self, player: Player) -> Card:
        player.add_card_to_hand(self.deck.draw_card())
        deck_size = self.deck.get_num_of_cards_in_deck()
        if deck_size == 0:
            pile = self.pile.get_pile()
            pile_top_card = pile.pop()
            self.pile.reset_pile()
            self.pile.add_to_pile(pile_top_card)
            self.deck.add_to_deck(pile)
            self.deck._shuffle_deck()
        self.redraw_game()

    def has_player_won(self, player: Player) -> bool:
        if player.get_how_many_cards_player_has() == 0:
            return True
        return False

    def redraw_game(self) -> None:
        self.renderer.render(self.deck, self.pile, self.chat, self.ai)