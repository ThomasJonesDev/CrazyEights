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

    def get_submitted_answers(self) -> list[tuple[int, str]]:
        """
        Tells TwitchConnection to stop recording messages from chat
        Calulates which card was selected the most and returns it as a tuple
        """
        self.twitch_connection.send_to_chat(STOP_SUBMITTING_ANSWER_MESSAGE)
        messages: list[str] = self.twitch_connection.get_messages_since_checkpoint()
        parsed_input: dict[str, str] = TwitchCrowdsourcing._parse_input(messages)
        filtered_input: dict[str, str] = TwitchCrowdsourcing._filter_answers(
            parsed_input
        )
        orderd_moves: list[str] = TwitchCrowdsourcing._get_list_of_choosen_cards(
            filtered_input
        )
        return TwitchCrowdsourcing._convert_card_str_to_tuple(orderd_moves)

    @staticmethod
    def _convert_card_str_to_tuple(card_list: list[str]) -> list[tuple[int, str]]:
        """
        ...
        """
        tuple_list: list[tuple[int, str]] = []
        for card in card_list:
            if len(card) == 3:
                tuple_list.append((10, card[2]))
            else:
                tuple_list.append((int(card[0]), card[1]))

        return tuple_list

    @staticmethod
    def _get_list_of_choosen_cards(chat_moves: dict[str, str]) -> list[str]:
        """
        ...
        """

        card_tally: dict[str, int] = TwitchCrowdsourcing._create_card_tally()

        # Get a list of all submitted cards
        for _, chat_val in chat_moves.items():
            for tally_key, _ in card_tally.items():
                if chat_val == tally_key:
                    card_tally[tally_key] += 1
                    break

        # Remove cards with value of 0
        temp_dict: dict[str, int] = {}
        for key, value in card_tally.items():
            if value > 0:
                temp_dict[key] = value

        # Count how many times a card is selected
        sorted_list: list[str] = sorted(temp_dict, key=lambda x: x[1], reverse=True)
        return sorted_list

    @staticmethod
    def _create_card_tally() -> dict[str, int]:
        """
        Creates a directory that contains all 52 cards in a deck, move, num_of_votes
        """
        tally: dict[str, int] = {}
        for suit in SUITS:
            for value in VALUES:
                tally[value + suit] = 0
        return tally

    @staticmethod
    def _parse_input(messages: list[str]) -> dict[str, str]:
        """
        Returns a dictionary that contains username, message
        e.g.
        ":foo!foo@foo.tmi.twitch.tv PRIVMSG #bar :bleedPurple" -> { "foo" : "bleedPurple" }
        """
        parsed_input: dict[str, str] = {}
        for message in messages:
            split_message: list[str] = message.split(" :")
            temp: list[str] = split_message[0].split("!")
            username: str = temp[0]
            user_message: str = split_message[1]
            username = username[1:]
            parsed_input[username] = user_message

        return parsed_input

    @staticmethod
    def _filter_answers(dictionary: dict[str, str]) -> dict[str, str]:
        """
        Takes a dictionary and removes all the entries which dont have a valid value
        """
        filtered_dictionary: dict[str, str] = {}

        for player, answer in dictionary.items():
            answer = answer.upper()
            if len(answer) == 3:
                for suit in SUITS:
                    if answer[0] == "1" and answer[1] == "0":
                        if answer[2] == suit:
                            filtered_dictionary[player] = answer
            elif len(answer) == 2:
                for suit in SUITS:
                    for value in VALUES:
                        if answer[0] == value and answer[1] == suit:
                            filtered_dictionary[player] = answer

        return filtered_dictionary
