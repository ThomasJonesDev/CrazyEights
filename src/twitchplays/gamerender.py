from typing import TYPE_CHECKING

from pygame import display, font, image

if TYPE_CHECKING:
    from pygame.font import Font
    from pygame.surface import Surface

    from .card import Card
    from .deck import Deck
    from .pile import Pile
    from .player import Player


class GameRenderer:

    def __init__(self) -> None:
        window_width: int = 1920
        window_height: int = 1080
        window_caption: str = "Twitch Plays"
        self._back_of_card_image: "Surface" = image.load(
            "images/Playing Cards/card-back1.png"
        )
        self._display: "Surface" = display.set_mode((window_width, window_height))
        display.set_caption(window_caption)
        self._text_font: "Font" = font.Font("fonts/ProtestStrike-Regular.ttf", 32)

    def draw_player_one_cards(self, playing_hand: list["Card"]) -> None:
        for index in range(len(playing_hand)):
            self._display.blit(
                playing_hand[index].get_card_image(), (320 + (index * 100), 800)
            )

    def draw_player_two_cards(self, playing_hand: list["Card"]) -> None:
        for index in range(len(playing_hand)):
            self._display.blit(self._back_of_card_image, (320 + (index * 100), 200))

    def draw_back_of_card(self, x: int, y: int) -> None:
        self._display.blit(self._back_of_card_image, (x, y))

    def draw_background(self) -> None:
        background_colour: tuple[int, int, int] = (0, 255, 0)
        self._display.fill(background_colour)

    def draw_deck(self, game_deck: list["Card"]) -> None:
        x: int = 1600
        y: int = 540
        if len(game_deck) > 0:
            self._display.blit(self._back_of_card_image, (x, y))

    def draw_pile(self, game_pile: list["Card"]) -> None:
        x: int = 640
        y: int = 540
        if len(game_pile) > 0:
            self._display.blit(game_pile[-1].get_card_image(), (x, y))

    def render_time_remaining(self, time_in_seconds: int) -> None:
        x: int = 600
        y: int = 100
        text_colour: tuple[int, int, int] = (255, 0, 0)
        time_text: Surface = self._text_font.render(
            "Time remaining to select a card is: " + str(time_in_seconds) + " seconds.",
            True,
            text_colour,
        )
        self._display.blit(time_text, (x, y))
        display.update()

    def render(
        self,
        game_deck: "Deck",
        game_pile: "Pile",
        player_one: "Player",
        player_two: "Player",
    ) -> None:
        self.draw_background()
        self.draw_deck(game_deck.get_deck())
        self.draw_pile(game_pile.get_pile())
        self.draw_player_one_cards(player_one.get_player_hand())
        self.draw_player_two_cards(player_two.get_player_hand())
        display.update()
