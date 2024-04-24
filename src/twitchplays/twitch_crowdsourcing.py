from .twitchconnection import TwitchConnection

START_SUBMITTING_MSG: str = (
    "ENTER WHAT MOVE YOU WANT TO PLAY e.g. 'KS' for King of Spades or '10H for Ten of Hearts"
)

STOP_SUBMITTING_MSG: str = "YOU CAN NO LONGER SUBMIT MOVES"

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
    """Takes the raw data from Twitch IRC servers, then filter and parse results and return a list of moves"""

    def __init__(self) -> None:
        """Initiate twitch_connection class to connect to Twitch"""
        self._twitch_connection = TwitchConnection()

    def start_collecting_answers(self) -> None:
        """Sends message to chat telling users to start entering their choosen card in the chat
        Empties lists so only recieve messages recieved in the given time.
        """
        self._twitch_connection.send_to_chat(START_SUBMITTING_MSG)
        self._twitch_connection.clear_irc_msgs()

    def get_submitted_answers(self) -> list[tuple[int, str]]:
        """Gets raw data from Twitch, call functions to filter and parse data, returns cards in format that the game can use

        Returns:
            list[tuple[int, str]]: list of cards represented by tuples. Each tuple is the value and suit of a card.
        """
        self._twitch_connection.send_to_chat(STOP_SUBMITTING_MSG)
        messages: list[str] = self._twitch_connection.get_irc_msgs()
        print(messages)
        parsed_input: dict[str, str] = TwitchCrowdsourcing._parse_input(messages)
        print(parsed_input)
        filtered_input: dict[str, str] = TwitchCrowdsourcing._filter_answers(
            parsed_input
        )
        print(filtered_input)
        orderd_moves: list[str] = TwitchCrowdsourcing._get_list_of_choosen_cards(
            filtered_input
        )
        print(orderd_moves)
        return TwitchCrowdsourcing._convert_card_str_to_tuple(orderd_moves)

    @staticmethod
    def _convert_card_str_to_tuple(card_list: list[str]) -> list[tuple[int, str]]:
        """Takes the string representation of a card and turns it into a tuple
        e.g. "5S" -> (5, "S")

        Args:
            card_list (list[str]): A list of cards represented by cards e.g. "5S"

        Returns:
            list[tuple[int, str]]: A list of cards represented by tuples e.g. (5,"S")
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
        """Takes a dictionary of a players name and what card they choose, returns a list of cards sorted by popularity

        Args:
            chat_moves (dict[str, str]): A dictionary of players and their choosen card e.g. {"Bob": "QS", ...}

        Returns:
            list[str]: A list of cards represented as strings, orded by most popular (index 0) to least popular (index n)
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
        """Creates a dictionary that will be used as a tally for each card

        Returns:
            dict[str, int]: dictionary that contains a string representation and a tally value e.g. {"AC": 0, ...}
        """
        tally: dict[str, int] = {}
        for suit in SUITS:
            for value in VALUES:
                tally[value + suit] = 0
        return tally

    @staticmethod
    def _parse_input(messages: list[str]) -> dict[str, str]:
        """Parses the raw messages from Twitch, returns a dictionary that contains twitch usernames and their message
        The use of dictionary stops a user from having mulitiple "votes"

        Args:
            messages (list[str]): e.g. [":foo!foo@foo.tmi.twitch.tv PRIVMSG #bar :bleedPurple"]
        Returns:
            dict[str, str]: e.g. {"foo": "bleedPurple"}
        """
        parsed_input: dict[str, str] = {}

        if len(messages) == 0:
            return parsed_input
        for message in messages:
            split_message: list[str] = message.split(" :")
            temp: list[str] = split_message[0].split("!")
            username: str = temp[0]
            user_message: str = split_message[1].rstrip()  # rstrip remove \r\n
            username = username[1:]
            parsed_input[username] = user_message

        return parsed_input

    @staticmethod
    def _filter_answers(dictionary: dict[str, str]) -> dict[str, str]:
        """Checks each message in the dictionary and remove any messages that dont follow the required format to choose a card e.g. "5S" for 5 of spades

        Args:
            dictionary (dict[str, str]): dictionary of twitch-username : message

        Returns:
            dict[str, str]: filtered dictionary of twitch-username : message
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

    def diconnect(self) -> None:
        """Tells twitch_connection to diconnect from Twitch IRC servers"""
        self._twitch_connection.disconnect()
