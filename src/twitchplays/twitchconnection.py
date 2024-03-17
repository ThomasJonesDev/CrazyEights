import os
import socket
import threading
from threading import Thread

from dotenv import load_dotenv

CRLF = "\r\n"
ENCODING_FORMAT = "utf-8"
MAX_BYTES = 512
TWITCH_IRC_URI = "irc.chat.twitch.tv"
TWITCH_IRC_PORT = 6667


class TwitchConnection(Thread):
    """
    To get OAUTH CODE use the follow link:
    https://id.twitch.tv/oauth2/authorize?response_type=token&redirect_uri=http://localhost:3000&client_id=0v3q3zcud5b4x3o7tf4olkc0mt7cpo&scope=chat%3Aread+chat%3Aedit
    """

    def __init__(self):
        # Global variables
        self.message_log: list[str] = []

        # Set up connection with Twitch.tv
        load_dotenv()
        oauth = f"oauth:{os.getenv('OAUTH')}"
        channel = os.getenv("CHANNEL")
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
        self.irc.sendall(f"JOIN #{channel}{CRLF}".encode(ENCODING_FORMAT))
        threading.Thread(self.listen_for_incomming_messages())

    def listen_for_incomming_messages(self) -> None:
        while True:
            recieved_message = self.irc.recv(MAX_BYTES).decode(ENCODING_FORMAT)
            self.message_log.append(recieved_message)
            print(recieved_message)
            if recieved_message.startswith("PING"):
                irc.sendall(f"PONG :tmi.twitch.tv{CRLF}".encode(ENCODING_FORMAT))
                print(f"PONG :tmi.twitch.tv{CRLF}")
                # TODO ADD THREADING

    def add_logging_checkpoint(self) -> None:
        """ """
        self.message_log.append("#LOGGING:CHECKPOINT#")

    def get_messages_since_checkpoint(self) -> list[str]:
        pass


# Allow running module independently to allow testing
if __name__ == "__main__":
    TwitchConnection()
