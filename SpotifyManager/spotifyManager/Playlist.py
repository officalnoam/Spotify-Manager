from typing import List
from spotipy import Spotify

from .Song import Song


class Playlist:
    def __init__(self, spotify: Spotify, playlistId: str):
        self._spotify = spotify
        self.id = playlistId

        _playlist = self._spotify.playlist(self.id)

        self.name = _playlist['name']
        self.songs = self._getPlaylistSongs()

    def _getPlaylistSongs(self) -> List[Song]:
        songs = self._spotify.playlist_items(self.id)
        offset = 100
        songList = []
        while len(songs['items']) != 0:
            for song in songs['items']:
                if 'track' not in song.keys() or not isinstance(song['track'], dict) or any(dictKey not in song['track'].keys() for dictKey in ['id', 'name']):
                    continue
                songList.append(Song(song['track']))
            songs = self._spotify.playlist_items(self.id, offset=offset)
            offset += 100
        
        return songList