import time


class Countdown:

    def __init__(self) -> None:
        self._start_time: float = -1
        self._countdown_duration: int = 1
        self._countdown_active = False

    def get_start_time(self) -> float:
        return self._start_time

    def start_countdown(self) -> None:
        self._countdown_active = True
        self._start_time = time.time()

    def get_countdown_in_seconds(self) -> int:
        elapsed_time: int = int(time.time() - self._start_time)
        return max(0, self._countdown_duration - elapsed_time)

    def is_countdown_running(self) -> bool:
        return self._countdown_active

    def stop_countdown(self) -> None:
        self._countdown_active = False
