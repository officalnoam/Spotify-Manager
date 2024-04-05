from typing import Dict


class Song:
    def __init__(self, spotifyApiSong: Dict[str, str]):
        self.id = spotifyApiSong['id']
        self.name = spotifyApiSong['name']