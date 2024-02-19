from unittest import TestCase
from crowdsourcing import CrowdSourcing


class TestCrowdSourcing(TestCase):
    def test_convert_answer_string_to_tuple(self):
        input_string = "AS"
        output_tuple = (1, 'S')
        self.assertEqual(output_tuple, CrowdSourcing.convert_answer_string_to_tuple(input_string))

    def test_filter_answers(self):
        self.assertEqual(None, CrowdSourcing.filter_answers(""))
        self.assertEqual(None, CrowdSourcing.filter_answers("10"))
        self.assertEqual(None, CrowdSourcing.filter_answers("h392y"))
        self.assertEqual("10S", CrowdSourcing.filter_answers("10S"))
        self.assertEqual("AS", CrowdSourcing.filter_answers("AS"))
        self.assertEqual("5D", CrowdSourcing.filter_answers("5d"))
