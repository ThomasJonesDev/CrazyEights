import os
import socket
from threading import Thread

from dotenv import load_dotenv

CRLF = "\r\n"
ENCODING = "utf-8"
MAX_BYTES = 512
TWITCH_IRC_URI = "irc.chat.twitch.tv"
TWITCH_IRC_PORT = 6667


class TwitchConnection(Thread):
    """
    Connects and authenitcates with Twitch.tv IRC server, then connects to twitch channel in .env file

    .env FILE REQUIRED: create file in same directory as this module with the following ENCODING
    OAUTH=<oauth code>
    CHANNEL=<channel name>

    To get OAUTH CODE use the follow link:
    https://id.twitch.tv/oauth2/authorize?response_type=token&redirect_uri=http://localhost:3000&client_id=0v3q3zcud5b4x3o7tf4olkc0mt7cpo&scope=chat%3Aread+chat%3Aedit
    """

    def __init__(self) -> None:
        """
        ...
        """
        # Global variables
        self._irc_msgs: list[str] = []
        # Use .env file to allow for code to be shared without sharing oauth codes
        load_dotenv()
        oauth = f"oauth:{os.getenv('OAUTH')}"
        self.channel = os.getenv("CHANNEL")

        # Connect the bot to the channel
        self._irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._irc.connect((TWITCH_IRC_URI, TWITCH_IRC_PORT))

        self._irc.sendall(f"PASS {oauth}{CRLF}".encode(ENCODING))
        self._irc.sendall(f"NICK sgjone5{CRLF}".encode(ENCODING))

        # recieve the confirmation that the authenitcation was successful
        recv_msg: str = self._irc.recv(MAX_BYTES).decode(ENCODING)
        print(recv_msg)
        self._irc_msgs.append(recv_msg)

        # Join the chat
        self._irc.sendall(f"JOIN #{self.channel}{CRLF}".encode(ENCODING))
        listener = Thread(target=self.listen_for_irc_msgs, args=())
        listener.start()

    def listen_for_irc_msgs(self) -> None:
        """
        Recieves any messages from Twitch.tv and stores them in self._irc_msgs
        Is threaded to allow it to run parallel to the game.
        """
        while True:
            recv_msg: str = self._irc.recv(MAX_BYTES).decode(ENCODING)
            print(recv_msg)
            if recv_msg.startswith("PING"):
                self._irc.sendall(f"PONG :tmi.twitch.tv{CRLF}".encode(ENCODING))
                print(f"PONG :tmi.twitch.tv{CRLF}")
            else:
                self._irc_msgs.append(recv_msg)

    def send_to_chat(self, message: str) -> None:
        """
        ...
        """
        self._irc.sendall(f"PRIVMSG #{self.channel} :{message}{CRLF}".encode(ENCODING))

    def clear_irc_msgs(self) -> None:
        """
        ...
        """
        self._irc_msgs = []

    def get_irc_msgs(self) -> list[str]:
        """
        Returns all items in self._irc_msgs
        """
        return self._irc_msgs

    def disconnect(self) -> None:
        """
        ...
        """
        self._irc.sendall(f"PART{CRLF}".encode(ENCODING))
        self._irc.close()


# Allow running module independently to allow testing
if __name__ == "__main__":
    TwitchConnection()
