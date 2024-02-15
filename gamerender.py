import pygame.display


class GameRenderer:

    def __init__(self):
        window_width = 1920
        window_height = 1080
        window_caption = "Twitch Plays"
        self.back_of_card_image = pygame.image.load('images/Playing Cards/card-back1.png')
        self.display = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(window_caption)
        self.text_font = pygame.font.Font("fonts/ProtestStrike-Regular.ttf", 32)

    def draw_player_one_cards(self, playing_hand):
        for index in range(len(playing_hand)):
            self.display.blit(playing_hand[index].get_card_image(), (320 + (index * 100), 800))

    def draw_player_two_cards(self, playing_hand):
        for index in range(len(playing_hand)):
            self.display.blit(self.back_of_card_image, (320 + (index * 100), 200))

    def draw_back_of_card(self, x, y):
        self.display.blit(self.back_of_card_image, (x, y))

    def draw_background(self):
        background_colour = [0, 255, 0]
        self.display.fill(background_colour)

    def draw_deck(self, deck):
        x = 1600
        y = 540
        if deck is not None:
            self.display.blit(self.back_of_card_image, (x, y))

    def draw_pile(self, pile):
        x = 640
        y = 540
        if pile is not None:
            self.display.blit(pile[-1].get_card_image(), (x, y))

    def render_time_remaining(self, time_in_seconds):
        x = 600
        y = 100
        text_colour = [255, 0, 0]
        time_text = self.text_font.render(
            "Time remaining to select a card is: " + str(time_in_seconds) + " seconds.", True, text_colour)
        self.display.blit(time_text, (x, y))
        pygame.display.update()

    def render(self, deck, pile, player_one_hand, player_two_hand):
        self.draw_background()
        self.draw_deck(deck)
        self.draw_pile(pile)
        self.draw_player_one_cards(player_one_hand)
        self.draw_player_two_cards(player_two_hand)
        pygame.display.update()

