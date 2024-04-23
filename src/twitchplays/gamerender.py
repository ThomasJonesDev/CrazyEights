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
    """Class that does all the GUI rendering"""

    def __init__(self) -> None:
        """Creates the window, and initialises font and caption"""
        self._window_width: int = 1920
        self._window_height: int = 1080
        window_caption: str = "Twitch Plays"
        self._back_of_card_image = image.load("./src/images/cards/card-back1.png")
        self._display = display.set_mode((self._window_width, self._window_height))
        display.set_caption(window_caption)
        self._text_font: "Font" = font.Font("./src/fonts/ProtestStrike-Regular.ttf", 32)
        self.draw_background()
        display.update()

    def _draw_twitch_cards(self, playing_hand: list["Card"]) -> None:
        """Draw the cards in the hand of Twitch

        Args:
            playing_hand (list[Card]): a list of card objects in Twitch's hand
        """
        num_of_cards: int = len(playing_hand)
        for index in range(num_of_cards):
            img = playing_hand[index].get_card_image()
            gap: float = 1.2
            img_width = img.get_width()
            img_height = img.get_height()
            x: int = (
                (self._window_width / 2)
                - ((num_of_cards / 2) * (img_width * gap))
                + (index * (img_width * gap))
            )
            y: int = (self._window_height * 0.75) - (img_height / 2)
            self._display.blit(img, (x, y))

    def _draw_ai_cards(self, playing_hand: list["Card"]) -> None:
        """draws the back of the cards in ai hand

        Args:
            playing_hand (list[Card]): a list of card objects in the AI's hand
        """
        for index in range(len(playing_hand)):
            img = self._back_of_card_image
            gap: float = 1.2
            no_cards: int = len(playing_hand)
            img_width = img.get_width()
            img_height = img.get_height()
            x: float = (
                (self._window_width / 2)
                - ((no_cards / 2) * (img_width * gap))
                + (index * (img_width * gap))
            )
            y: float = (self._window_height * 0.25) - (img_height / 2)
            self._display.blit(img, (x, y))

    def _draw_back_of_card(self, x: int, y: int) -> None:
        """_summary_

        Args:
            x (int): the x coordinate
            y (int): the y coordinate
        """
        self._display.blit(self._back_of_card_image, (x, y))

    def draw_background(self) -> None:
        """Draws the background"""
        background_colour: tuple[int, int, int] = (0, 255, 0)
        # Get size of back ground
        (self._window_width, self._window_height) = display.get_surface().get_size()
        self._display.fill(background_colour)

    def _draw_deck(self, game_deck: list["Card"]) -> None:
        """Draws the deck (shows back of the top card)

        Args:
            game_deck (list[Card]): list of the card objects in the deck
        """
        img = self._back_of_card_image
        x: int = (self._window_width * 0.6) - (img.get_width() * 0.5)
        y: int = (self._window_height * 0.5) - (img.get_height() * 0.5)
        if len(game_deck) > 0:
            self._display.blit(img, (x, y))

    def _draw_pile(self, game_pile: list["Card"]) -> None:
        """Draaws the pile (shows the front of the top card)

        Args:
            game_pile (list[Card]): list of the card objects on the pile
        """
        img = game_pile[-1].get_card_image()
        x: float = (self._window_width * 0.4) - (img.get_width() * 0.5)
        y: float = (self._window_height * 0.5) - (img.get_height() * 0.5)
        if len(game_pile) > 0:
            self._display.blit(img, (x, y))

    def render_time_remaining(self, time_in_seconds: int) -> None:
        """Shows how many seconds remaining that Twitch chat has to choose their card

        Args:
            time_in_seconds (int): time remaining in seconds
        """
        x: float = self._window_width * 0.5
        y: float = self._window_height * 0.1
        text_colour: tuple[int, int, int] = (255, 0, 0)
        time_text: Surface = self._text_font.render(
            "Time remaining to select a card is: " + str(time_in_seconds) + " seconds.",
            True,
            text_colour,
        )
        text_rect = time_text.get_rect(center=(x, y))
        self._display.blit(time_text, text_rect)
        display.update()

    def render(
        self,
        game_deck: "Deck",
        game_pile: "Pile",
        player_one: "Player",
        player_two: "Player",
    ) -> None:
        """renders the background, payers cards, deck, and pile.

        Args:
            game_deck (Deck): _description_
            game_pile (Pile): _description_
            player_one (Player): _description_
            player_two (Player): _description_
        """
        self.draw_background()
        self._draw_deck(game_deck.get_deck())
        self._draw_pile(game_pile.get_pile())
        self._draw_twitch_cards(player_one.get_hand())
        self._draw_ai_cards(player_two.get_hand())
        display.update()

    def render_message(self, message: str) -> None:
        """Displays a message to screen

        Args:
            message (str): The message to be shown
        """
        x: float = self._window_width * 0.5
        y: float = self._window_height * 0.5
        text_colour: tuple[int, int, int] = (255, 0, 0)
        text: Surface = self._text_font.render(
            "" + message + "",
            True,
            text_colour,
        )
        text_rect = text.get_rect(center=(x, y))

        self.draw_background()
        self._display.blit(text, text_rect)
        display.update()
