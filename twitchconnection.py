import asyncio
import os
import requests
import socket
from dotenv import load_dotenv

ENV_FILE = ".env"
TWITCH_OAUTH_LINK = "https://id.twitch.tv/oauth2/token"
TWITCH_IRC_URI = "irc.chat.twitch.tv"
TWITCH_IRC_PORT = 6667
ENCODING_FORMAT = "utf-8"


class TwitchConnection:

    def __init__(self):
        load_dotenv()
        oauth = os.getenv("OAUTH")
        # Connect the bot to the channel
        irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        irc.connect((TWITCH_IRC_URI, TWITCH_IRC_PORT))

        irc.send(f"PASS {oauth}".encode(ENCODING_FORMAT))
        irc.send(f"NICK bot".encode(ENCODING_FORMAT))
        


TwitchConnection()
