# TwitchPlays

A game of crazy eights that you can stream to your twitch chat, which they can then interact with using the chat.

## Installation

Ensure you have the latest version of Python installed.
```bash
sudo apt update
sudo apt upgrade
sudo apt install python3.11
```

Then copy Twitch plays onto your computer.

Enter the working directory
```bash
cd TwitchPlays
```

Next set up a virtual enviroment for Twitch Plays to run in.
```bash
python -m venv .
```

Then install the dependencies
```bash
pip install -r requirements.txt
```

Next create a .env file that contains the following
OAUTH=<oauth-code>
CHANNEL=<channel-name>

Where CHANNEL is the name of your twitch account.
To get your OAUTH code click on the following link, and sign in to Twitch. Once you have done that, you will be redirected to localhost:3000 where the OAUTH code will be in the URL.

https://id.twitch.tv/oauth2/authorize?response_type=token&redirect_uri=http://localhost:3000&client_id=0v3q3zcud5b4x3o7tf4olkc0mt7cpo&scope=chat%3Aread+chat%3Aedit


## Usage

To run the program whiles inside the virtual enviroment and the working directory

```bash
python3 main.py
```