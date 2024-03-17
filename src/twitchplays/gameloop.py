import pygame

from .countdown import Countdown
from .crazyeights import CrazyEights
from .crowdsourcing import CrowdSourcing
from .deck import Deck
from .gamerender import GameRenderer
from .gamestate import GameState
from .pile import Pile
from .player import Player

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
GAME_TITLE = "Twitch Plays"
FPS = 1
BACKGROUND_COLOUR = [0, 255, 0]
BACK_OF_CARD = pygame.image.load("images/Playing Cards/card-back1.png")
NUMBER_OF_STARTING_CARDS = 7


def game_loop():
    # Initialise the game
    pygame.init()
    # Initialise the game render
    game_renderer = GameRenderer()
    clock = pygame.time.Clock()
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
    for _ in range(NUMBER_OF_STARTING_CARDS):
        twitch_player.add_card_to_hand(deck.draw_card())
        ai_player.add_card_to_hand(deck.draw_card())

    # Put first card onto the pile
    pile.add_to_pile(deck.draw_card())

    # Start game state in player ones(twitch) go.
    game_state = GameState.TWITCH_PLAYING

    game_over = False
    while not game_over:

        # Render the game
        game_renderer.render(deck, pile, twitch_player, ai_player)
        if (
            countdown.is_countdown_running() is True
            and countdown.get_countdown_in_seconds() >= 0
        ):
            game_renderer.render_time_remaining(countdown.get_countdown_in_seconds())

        # Process Mouse/Keyboard Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Update Game
        if game_state is GameState.TWITCH_PLAYING:

            # Check if player has any valid moves, if not take card from deck
            if (
                CrazyEights.check_if_any_valid_moves(
                    twitch_player.get_player_hand(), pile.get_top_card()
                )
                is False
            ):
                twitch_player.add_card_to_hand(deck.draw_card())
                continue  # continue to skip rest of loop to prevent counter from starting

            # 30-Second countdown
            if not countdown.is_countdown_running():
                countdown.start_countdown()
            if (
                countdown.is_countdown_running() is True
                and countdown.get_countdown_in_seconds() <= 0
            ):
                countdown.stop_countdown()
                # Get the input from Twitch
                crowdsourced_answer = crowdsourcing.get_crowdsourced_answer()
                selected_card = None
                while selected_card == None:
                    selected_card = CrazyEights.get_select_card(
                        crowdsourced_answer, twitch_player.get_player_hand()
                    )

                # If there is a valid card played, then play card and switch to AI's go
                if CrazyEights.is_valid_move(selected_card, pile.get_top_card()):
                    pile.add_to_pile(twitch_player.play_card(selected_card))

                # Check win conditions for Twitch Player
                if twitch_player.get_how_many_cards_player_has() == 0:
                    # Send message saying congratulations and break game loop
                    print(
                        "Twitch Player wins"
                    )  # TODO change this to a win message using render class
                    break
        elif game_state is GameState.AI_PLAYING:
            # TODO get input and update game state
            pass

        # Set to 1 FPS to prevent flickering when the timer is updating, aswell as no reason to update more frequently
        clock.tick(FPS)

    # TODO implement game over screen with the winner
