import time


class Countdown:
    """_summary_"""

    def __init__(self) -> None:
        """_summary_"""
        self._start_time: int = -1
        self._countdown_duration: int = 1
        self._countdown_active: bool = False

    def get_start_time(self) -> float:
        """_summary_

        Returns:
            float: _description_
        """
        return self._start_time

    def start_countdown(self) -> None:
        """_summary_"""
        self._countdown_active = True
        self._start_time = time.time()

    def get_seconds_remaining(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        elapsed_time: int = int(time.time() - self._start_time)
        return max(0, self._countdown_duration - elapsed_time)

    def is_countdown_running(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return self._countdown_active

    def stop_countdown(self) -> None:
        """_summary_"""
        self._countdown_active = False
