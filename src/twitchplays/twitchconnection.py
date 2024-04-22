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
    """Connects and authenitcates with Twitch.tv IRC server, to read and write to chat

    Args:
        Thread (Thread): TwitchConnection extends Thread
    """

    def __init__(self) -> None:
        """Using IRC protocol, connect and authenticate with Twitch.tv IRC servers"""
        # Global variables
        self._irc_msgs: list[str] = []
        # Use .env file to allow for code to be shared without sharing oauth codes
        load_dotenv()
        oauth = f"oauth:{os.getenv('OAUTH')}"
        self._channel = os.getenv("CHANNEL")

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
        self._irc.sendall(f"JOIN #{self._channel}{CRLF}".encode(ENCODING))
        # Create a listener
        listener = Thread(target=self._listen_for_irc_msgs, args=())
        listener.start()

    def _listen_for_irc_msgs(self) -> None:
        """A listener function on its own thread.
        If incomming message is PING reply with PONG to keep connection alive,
        otherwise stores any incoming messages to self._irc_msgs.
        Function runs on its own thread to allow rest of program to keep running
        as socket.recv is a blocking functions
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
        """Sends a message to the chat

        Args:
            message (str): message to send to chat
        """
        self._irc.sendall(f"PRIVMSG #{self._channel} :{message}{CRLF}".encode(ENCODING))

    def clear_irc_msgs(self) -> None:
        """Set self._irc_msgs to a empty list"""
        self._irc_msgs: list[str] = []

    def get_irc_msgs(self) -> list[str]:
        """Returns self._irc_msgs list

        Returns:
            list[str]: messages in self._irc_msgs.
        """
        return self._irc_msgs

    def disconnect(self) -> None:
        """Send message to Twitch IRC to diconnect bot. Then closes socket connection"""
        self._irc.sendall(f"PART{CRLF}".encode(ENCODING))
        self._irc.close()


# Allow running module independently to allow testing
if __name__ == "__main__":
    TwitchConnection()
