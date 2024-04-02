import os

from json import load


class SpotifySessionConsts:
    with open(f"{os.path.abspath(os.path.dirname(__file__))}/secrets.json", "r") as f:
        secrets = load(f)
    ID = secrets["client id"]
    SECRET = secrets["client secret"]
    URL = secrets["redirect url"]
    SCOPE = secrets["scope"]

    del(f)
    del(secrets)