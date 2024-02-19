from card import Card
from typing import Any


class CrowdSourcing:

    def __init__(self):
        # TODO Establish a connection to twitch
        pass

    def get_crowdsourced_answer(self) -> tuple[int, chr]:
        # TODO Validate answers
        # TEMP SOLUTION WHILES IN DEVELOPMENT
        return self.convert_answer_string_to_tuple(self.get_input_via_cli())

    @staticmethod
    def get_input_via_cli() -> str:
        answer = input("Enter which card you would like to play")
        return answer

    @staticmethod
    def convert_answer_string_to_tuple(answer_string: str) -> tuple[int, chr]:
        number: int = 0
        multiply_factor: int = 1
        counter: int = 0
        for character in answer_string:
            if character.isnumeric():
                number = (number * multiply_factor) + int(character)
                multiply_factor *= 10
                counter += 1
            else:
                break

        if number == 0:
            number = Card.get_face_card_value(answer_string[0])
            counter += 1

        return number, answer_string[counter]

    @staticmethod
    def filter_answers(inputted_string: str) -> str:
        values: tuple[Any, ...] = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
        suits: tuple[chr, ...] = ('S', 'D', 'H', 'S')
        inputted_string = inputted_string.upper()
        if len(inputted_string) == 3:
            for suit in suits:
                if inputted_string[0] == '1' and inputted_string[1] == '0':
                    if inputted_string[2] == suit:
                        return inputted_string
        elif len(inputted_string) == 2:
            for suit in suits:
                for value in values:
                    if inputted_string[0] == value and inputted_string[1] == suit:  #
                        return inputted_string
