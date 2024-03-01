import asyncio
import os
import requests
import socket
import webbrowser
from dotenv import load_dotenv

ENV_FILE = ".env"
TWITCH_OAUTH_LINK = "https://id.twitch.tv/oauth2/authorize"
TWITCH_IRC_URI = "irc.chat.twitch.tv"
TWITCH_IRC_PORT = 6667
ENCODING_FORMAT = "utf-8"
CRLF = "\r\n"
ENV_FILE = ".env"
CLIENT_ID = "0v3q3zcud5b4x3o7tf4olkc0mt7cpo"
LOCAL_HOST_IP = "127.0.0.1"
LOCAL_HOST_PORT = 3000
REDIRECT_URI = "http://localhost:3000"

SCOPE = "chat%3Aread+chat%3Aedit"



class TwitchConnection:

    def __init__(self):
        load_dotenv()
        oauth = os.getenv("OAUTH")
        # Connect the bot to the channel
        irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        irc.connect((TWITCH_IRC_URI, TWITCH_IRC_PORT))

        irc.sendall(f"PASS {oauth}{CRLF}".encode(ENCODING_FORMAT))
        irc.sendall(f"NICK bot{CRLF}".encode(ENCODING_FORMAT))

        # recieve the confirmation that the authenitcation was successful
        authentication_confirmation = irc.recv(512).decode(ENCODING_FORMAT)
        print(authentication_confirmation)

        # Join the chat
        irc.sendall(f"JOIN #sgtjone5 {CRLF}")
        # Sends a message to the twitch chat when it connects
        # irc.sendall(f"PRIVMSG #sgtjone5{CRLF}".encode(ENCODING_FORMAT))

        while True:
            recieved_message = irc.recv(2048).decode(ENCODING_FORMAT)
            print(recieved_message)
            if recieved_message.startswith("PING"):
                irc.sendall(f"PONG :tmi.twitch.tv{CRLF}".encode(ENCODING_FORMAT))
                print("PONG")

    def get_ouath() -> str:
        # Check if .env file exists
        if os.path.exists(ENV_FILE):
            # Get OAUTH from .env
            load_dotenv()
            oauth = os.getenv("OAUTH")
            # Check it is still valid

            # if invalid, refresh from twitch
        else:
            # TODO the following
            # Start a server on localhost to recieve results
            # Get OAUTH from Twitch
            webbrowser.open(f"{TWITCH_OAUTH_LINK}?"
                f"response_type=code&redirect_uri={REDIRECT_URI}&client_id={CLIENT_ID}&scope={SCOPE}")
            # Add to .env 
        return oauth


    @staticmethod
    def get_oauth_from_twitch() -> str:
        # Start server to listen to localhost to get response
        local_host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_host.bind((LOCAL_HOST_IP, LOCAL_HOST_PORT))
        local_host.listen()
        print("SERVER STARTED")

        # Get user to authenitcate twitch twitch
        webbrowser.open(f"{TWITCH_OAUTH_LINK}?"
            f"response_type=token&redirect_uri={REDIRECT_URI}&client_id={CLIENT_ID}&scope={SCOPE}")

        # Get response 
        connection, address = local_host.accept()
        data = connection.recv(4096).decode(ENCODING_FORMAT)

        # Use requests to send a GET request to own server to see what the url is on the server
        requests.get(REDIRECT_URI)
        print("DATA FROM TWITCH IS")
        print(f"{data} =====================================")
        local_host.close()
        return data



    @staticmethod
    def update_oauth_env_file(oauth: str) -> None:
        file = open(".env", "w+")
        file.write(f"OAUTH = {oauth}")
        file.close()


TwitchConnection.get_oauth_from_twitch()
