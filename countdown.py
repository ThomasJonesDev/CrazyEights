import time
import math


class Countdown:

    def __init__(self):
        self._start_time = None
        self._countdown_duration = 30

    def get_start_time(self):
        return self._start_time

    def start_countdown(self):
        self._start_time = time.time()

    def get_countdown_in_seconds(self):
        elapsed_time = time.time() - self._start_time
        return math.ceil(self._countdown_duration - elapsed_time)

    def stop_countdown(self):
        self._start_time = None
