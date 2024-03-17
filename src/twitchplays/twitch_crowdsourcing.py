from .twitchconnection import TwitchConnection

START_SUBMITTING_ANSWERS_MESSAGE: str = (
    "ENTER WHAT MOVE YOU WANT TO PLAY e.g. 'KS' for King of Spades or '10H for Ten of Hearts"
)
STOP_SUBMITTING_ANSWER_MESSAGE: str = "YOU CAN NO LONGER SUBMIT MOVES"
VALUES: tuple[str, ...] = (
    "A",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
)
SUITS: tuple[str, ...] = ("S", "C", "H", "D")


class TwitchCrowdsourcing:

    def __init__(self) -> None:
        """
        Establish a connection to twitch to get data from
        """
        self.twitch_connection = TwitchConnection()

    def start_collecting_answers(self) -> None:
        """
        Tells TwitchConnection to start recording messages in chat
        """
        self.twitch_connection.send_to_chat(START_SUBMITTING_ANSWERS_MESSAGE)
        self.twitch_connection.add_logging_checkpoint()

    def get_submitted_answers(self) -> tuple[int, str]:
        """
        Tells TwitchConnection to stop recording messages from chat
        Calulates which card was selected the most and returns it as a tuple
        """
        self.twitch_connection.send_to_chat(STOP_SUBMITTING_ANSWER_MESSAGE)
        messages: list[str] = self.twitch_connection.get_messages_since_checkpoint()
        parsed_input: dict[str, str] = self.parse_input(messages)
        filtered_input: dict[str, str] = self.filter_answers(parsed_input)
        mode_move: str = self.get_the_mode_move(filtered_input)
        return self.convert_mode_move_to_tuple(mode_move)

    @staticmethod
    def convert_mode_move_to_tuple(card: str) -> tuple[int, str]:
        """
        Takes the card represented as a string e.g. "10H" and returns it as a tuple (10, "H")
        """
        if len(card) == 3:
            return (10, card[2])
        return (int(card[0]), card[1])

    @staticmethod
    def get_the_mode_move(players_moves: dict[str, str]) -> str:
        """
        Gets the move that was choosen the most (the mode)
        """
        moves_counter: dict[str, int] = (
            TwitchCrowdsourcing.create_move_counter_dictionary()
        )

        for move in players_moves.values():
            moves_counter[move] = moves_counter[move] + 1

        return max(moves_counter)

    @staticmethod
    def create_move_counter_dictionary() -> dict[str, int]:
        """
        Creates a directory that contains all 52 cards in a deck, as the key
        set the value to 0 for all keys
        """
        move_counter: dict[str, int] = {}
        for suit in SUITS:
            for value in VALUES:
                move_counter[value + suit] = 0
        return move_counter

    @staticmethod
    def parse_input(messages: list[str]) -> dict[str, str]:
        """
        Returns a dictionary that contains username, message
        e.g.
        ":foo!foo@foo.tmi.twitch.tv PRIVMSG #bar :bleedPurple" -> { "foo" : "bleedPurple" }
        """
        parsed_input: dict[str, str] = {}
        for message in messages:
            split_message: list[str] = message.split(" :")
            temp: list[str] = split_message[0].split("!")
            username = (temp[0])[1:]
            user_message: str = split_message[1]
            parsed_input[username] = user_message

        return parsed_input

    @staticmethod
    def filter_answers(dictionary: dict[str, str]) -> dict[str, str]:
        """
        Takes a dictionary and removes all the entries which dont have a valid value
        """
        filtered_dictionary: dict[str, str] = {}

        for key, value in dictionary.items():
            inputted_string = value.upper()
            if len(inputted_string) == 3:
                for suit in SUITS:
                    if inputted_string[0] == "1" and inputted_string[1] == "0":
                        if inputted_string[2] == suit:
                            filtered_dictionary[key] = value
            elif len(inputted_string) == 2:
                for suit in SUITS:
                    for value in VALUES:
                        if inputted_string[0] == value and inputted_string[1] == suit:
                            filtered_dictionary[key] = value

        return filtered_dictionary
