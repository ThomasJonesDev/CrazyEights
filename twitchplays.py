import pygame

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
GAME_TITLE = "Twitch Plays"
FPS = 60
BACKGROUND_COLOUR = [0, 255, 0]


def game_loop():
    # Initialise the game
    pygame.init()
    window = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    pygame.display.set_caption(GAME_TITLE)

    clock = pygame.time.Clock()

    # Game Loop
    game_over = False
    while not game_over:
        # Draw assets on screen
        window.fill(BACKGROUND_COLOUR)

        clock.tick()
        pygame.display.update()
