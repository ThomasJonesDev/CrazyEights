import os
import socket
from threading import Thread

from dotenv import load_dotenv

CRLF = "\r\n"
ENCODING_FORMAT = "utf-8"
LOG_CHECKPOINT = "#LOGGING:CHECKPOINT#"
MAX_BYTES = 512
TWITCH_IRC_URI = "irc.chat.twitch.tv"
TWITCH_IRC_PORT = 6667


class TwitchConnection(Thread):
    """
    Connects and authenitcates with Twitch.tv IRC server, then connects to twitch channel in .env file

    .env FILE REQUIRED: create file in same directory as this module with the following ENCODING_FORMAT
    OAUTH=<oauth code>
    CHANNEL=<channel name>

    To get OAUTH CODE use the follow link:
    https://id.twitch.tv/oauth2/authorize?response_type=token&redirect_uri=http://localhost:3000&client_id=0v3q3zcud5b4x3o7tf4olkc0mt7cpo&scope=chat%3Aread+chat%3Aedit
    """

    def __init__(self) -> None:
        # Global variables
        self.message_log: list[str] = []

        # Use .env file to allow for code to be shared without sharing oauth codes
        load_dotenv()
        oauth = f"oauth:{os.getenv('OAUTH')}"
        self.channel = os.getenv("CHANNEL")

        # Connect the bot to the channel
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect((TWITCH_IRC_URI, TWITCH_IRC_PORT))

        self.irc.sendall(f"PASS {oauth}{CRLF}".encode(ENCODING_FORMAT))
        self.irc.sendall(f"NICK sgjone5{CRLF}".encode(ENCODING_FORMAT))

        # recieve the confirmation that the authenitcation was successful
        authentication_confirmation = self.irc.recv(MAX_BYTES).decode(ENCODING_FORMAT)
        print(authentication_confirmation)
        self.message_log.append(authentication_confirmation)

        # Join the chat
        self.irc.sendall(f"JOIN #{self.channel}{CRLF}".encode(ENCODING_FORMAT))
        listener = Thread(target=self.listen_for_incomming_messages, args=())
        listener.start()

    def listen_for_incomming_messages(self) -> None:
        """
        Recieves any messages from Twitch.tv and stores them in self.message_log
        Is threaded to allow it to run parallel to the game.
        """
        while True:
            recieved_message = self.irc.recv(MAX_BYTES).decode(ENCODING_FORMAT)
            print(recieved_message)
            if recieved_message.startswith("PING"):
                self.irc.sendall(f"PONG :tmi.twitch.tv{CRLF}".encode(ENCODING_FORMAT))
                print(f"PONG :tmi.twitch.tv{CRLF}")
            else:
                self.message_log.append(recieved_message)

    def send_to_chat(self, message: str) -> None:
        self.irc.sendall(
            f"PRIVMSG #{self.channel} :{message}{CRLF}".encode(ENCODING_FORMAT)
        )

    def add_logging_checkpoint(self) -> None:
        """Creates a checkpoint in self.message_log"""
        self.message_log.append(LOG_CHECKPOINT)

    def get_messages_since_checkpoint(self) -> list[str]:
        """
        Returns all items in self.message_log since the last checkpoint
        """
        last_checkpoint_index = -1
        for index, message in enumerate(reversed(self.message_log)):
            if message == LOG_CHECKPOINT:
                last_checkpoint_index = index
                break

        if last_checkpoint_index == -1:
            last_checkpoint_index = 0

        return self.message_log[last_checkpoint_index + 1 :]


# Allow running module independently to allow testing
if __name__ == "__main__":
    TwitchConnection()
