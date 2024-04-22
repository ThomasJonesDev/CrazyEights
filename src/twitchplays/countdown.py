import time


class Countdown:
    """Class that implements a countdown features"""

    def __init__(self) -> None:
        """Assign inital values"""
        self._start_time: float = -1
        self._countdown_duration: float = 3
        self._countdown_active: bool = False

    def start_countdown(self) -> None:
        """Starts coundown, by getting current time and setting countdown to be active"""
        self._countdown_active = True
        self._start_time = time.time()

    def get_seconds_remaining(self) -> int:
        """Calculates how many seconds are remaining on the countdown

        Returns:
            int: The number of seconds remaining
        """
        elapsed_time: float = float(time.time() - self._start_time)
        return max(0, int(self._countdown_duration - elapsed_time))

    def is_countdown_running(self) -> bool:
        """Checks if the countdown is currently running

        Returns:
            bool: True if running, else returns False
        """
        return self._countdown_active

    def stop_countdown(self) -> None:
        """Sets the countdown to be inactive"""
        self._countdown_active = False
