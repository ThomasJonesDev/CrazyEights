import os
import socket

from dotenv import load_dotenv

CRLF = "\r\n"
ENCODING_FORMAT = "utf-8"
MAX_BYTES = 512
TWITCH_IRC_URI = "irc.chat.twitch.tv"
TWITCH_IRC_PORT = 6667


class TwitchConnection:
    """
    To get OAUTH CODE use the follow link:
    https://id.twitch.tv/oauth2/authorize?response_type=token&redirect_uri=http://localhost:3000&client_id=0v3q3zcud5b4x3o7tf4olkc0mt7cpo&scope=chat%3Aread+chat%3Aedit
    """

    def __init__(self):
        load_dotenv()
        oauth = os.getenv("OAUTH")
        channel = os.getenv("CHANNEL")
        # Connect the bot to the channel
        irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        irc.connect((TWITCH_IRC_URI, TWITCH_IRC_PORT))

        irc.sendall(f"PASS {oauth}{CRLF}".encode(ENCODING_FORMAT))
        irc.sendall(f"NICK sgjone5{CRLF}".encode(ENCODING_FORMAT))

        # recieve the confirmation that the authenitcation was successful
        authentication_confirmation = irc.recv(MAX_BYTES).decode(ENCODING_FORMAT)
        print(authentication_confirmation)

        # Join the chat
        irc.sendall(f"JOIN #{channel}{CRLF}".encode(ENCODING_FORMAT))

        while True:
            recieved_message = irc.recv(MAX_BYTES).decode(ENCODING_FORMAT)
            print(recieved_message)
            if recieved_message.startswith("PING"):
                irc.sendall(f"PONG :tmi.twitch.tv{CRLF}".encode(ENCODING_FORMAT))
                print("PONG")
