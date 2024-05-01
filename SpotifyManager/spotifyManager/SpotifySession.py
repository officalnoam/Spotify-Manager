from typing import Dict, List

from spotipy import Spotify
from spotipy.util import prompt_for_user_token

from .Song import Song
from .Playlist import Playlist
from .CONSTS import SpotifySessionConsts
from .Utils.CliUtils import askMultipleChoiceQuestion, clearCli


class SpotifySession:
    def __init__(self, username: str):
        self.consts = SpotifySessionConsts()
        token = prompt_for_user_token(username=username, 
                                      scope=self.consts.SCOPE, 
                                      client_id=self.consts.ID, 
                                      client_secret=self.consts.SECRET, 
                                      redirect_uri=self.consts.URL)
        
        self.spotify = Spotify(token)

    def _getPlaylistsToIds(self) -> Dict[str, str]:
        """
        ::
            Get the playlist names to ids followed by the user.
        
        Returns:
            (Dict[str, str]):   A dict between playlist names followed by a user and their ids.
        """
        currentOffset = 0
        playlistsToIds = {}
        playlists = self.spotify.current_user_playlists()
        while playlists['items']:
            currentOffset += 50
            for playlist in playlists['items']:
                playlistsToIds[playlist['name']] = playlist['id']
            playlists = self.spotify.current_user_playlists(offset=currentOffset)
        return playlistsToIds
    
    def _getPlaylistsFromUserSelection(self, prompt: str) -> List[Playlist]:
        """
        ::
            Get a selection of playlists from the user- and then pull those playlists from spotify.
        
        Parameters:
            (str) prompt:       The prompt shown to the user when selecting the playlists.
    
        Returns:
            (List[Playlist]):   The playlists the user wants to sort.
        """
        playlistsToIds = self._getPlaylistsToIds()
        playlists = []

        clearCli()
        selectedPlaylists = askMultipleChoiceQuestion(prompt, options=list(playlistsToIds.keys()))

        clearCli()
        for playlistName in selectedPlaylists:
            print(f"Pulling playlist {playlistName} from spotify...")
            playlists.append(Playlist(self.spotify, playlistsToIds[playlistName]))
        
        clearCli()
        return playlists