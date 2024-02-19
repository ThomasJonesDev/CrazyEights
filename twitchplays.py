import pygame

from countdown import Countdown
from gamerender import GameRenderer
from player import Player
from deck import Deck
from pile import Pile
from gamestate import GameState
from crowdsourcing import CrowdSourcing
from crazyeights import CrazyEights

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
GAME_TITLE = "Twitch Plays"
FPS = 60
BACKGROUND_COLOUR = [0, 255, 0]
BACK_OF_CARD = pygame.image.load('images/Playing Cards/card-back1.png')
NUMBER_OF_STARTING_CARDS = 8


def game_loop():
    # Initialise the game
    pygame.init()
    # Initialise the game render
    game_renderer: 'GameRenderer' = GameRenderer()
    clock: 'Clock' = pygame.time.Clock()
    # Countdown timer
    countdown = Countdown()
    # Connect to Twitch
    crowdsourcing = CrowdSourcing()
    # Create players
    twitch_player = Player()
    ai_player = Player()

    # Create deck
    deck = Deck()

    # Create Pile
    pile = Pile()

    # Deal out starting cards
    for card_index in range(NUMBER_OF_STARTING_CARDS):
        twitch_player.add_card_to_hand(deck.draw_card())
        ai_player.add_card_to_hand(deck.draw_card())

    # Put first card onto the pile
    pile.add_to_pile(deck.draw_card())

    # Start game state in player ones(twitch) go.
    game_state = GameState.TWITCH_PLAYING

    game_over = False
    while not game_over:

        # Process Mouse/Keyboard Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Update Game
        if game_state is GameState.TWITCH_PLAYING:
            # TODO Fix the flickering with the countdown
            # 30 Second countdown
            if not countdown.is_countdown_running():
                countdown.start_countdown()
            if countdown.is_countdown_running() is True and countdown.get_countdown_in_seconds() <= 0:
                countdown.stop_countdown()
                # TODO take input and update game state
                crowdsourced_answer = crowdsourcing.get_crowdsourced_answer()
                selected_card = CrazyEights.get_select_card(crowdsourced_answer, twitch_player.get_player_hand())
                if CrazyEights.is_valid_move(selected_card, pile.get_pile()[-1]):
                    pile.add_to_pile(twitch_player.play_card(selected_card))
        elif game_state is GameState.AI_PLAYING:
            # TODO get input and update game state
            pass

        # Render TODO fix the flickering
        game_renderer.render(
            deck, pile, twitch_player, ai_player)
        if countdown.is_countdown_running() is True and countdown.get_countdown_in_seconds() >= 0:
            game_renderer.render_time_remaining(countdown.get_countdown_in_seconds())

        # Set to 1 FPS to prevent flickering when the timer is updating
        clock.tick(1)
