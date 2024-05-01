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
        self._username = username
        token = prompt_for_user_token(username=self._username, 
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
    
    @staticmethod
    def _getSongsToSort(playlistsToSort: List[Playlist], playlistsToSortInto: List[Playlist]) -> List[Song]:
        """
        ::
            Return a list of songs that need to be sorted. 
            The songs on the list must not already appear in the playlists the songs will be sorted into- and will only appear once.

        Parameters:
            (List[Playlist]) playlistsToSort:       The playlists that need to be sorted.
            (List[Playlist]) playlistsToSortInto:   The playlists that the songs will be sorted into.
        
        Returns:
            (List[Song]):                           A list of the songs that need to be sorted.
        """
        sortedSongs = []
        songsToSort = []

        for playlist in playlistsToSortInto:
            sortedSongs += playlist.songs

        for playlist in playlistsToSort:
            for song in playlist.songs:
                if song.name not in [existingSong.name for existingSong in sortedSongs] and song.name not in [sortedSong.name for sortedSong in songsToSort]:
                    songsToSort.append(song)

        return songsToSort
    
    def _addSongToPlaylist(self, playlistId: str, songId: str) -> None:
        """
        ::
            Add a song to a playlist.
        
        ParametersL
            (str) playlistId:   The playlist id.
            (str) songId:       The song id.
        """
        self.spotify.playlist_add_items(playlistId, [songId])

    def sortSongs(self) -> None:
        """
        Get from the user the playlists that need to be sorted, and the ones that need to be sorted into.
        Iterate over all songs that should be sorted- and give the user the option to sort the song into the playlists.
        Update the song immediately to the relevant playlist- so that if internet/power is cut- minimal sorting is lost.
        """

        playlistsToSort = self._getPlaylistsFromUserSelection("Choose the playlists to sort.")
        playlistsToSortInto = self._getPlaylistsFromUserSelection("Choose the playlists to sort into.")
        playlistsToSortIntoNamesToIds = {playlist.name: playlist.id for playlist in playlistsToSortInto}

        songsToSort = self._getSongsToSort(playlistsToSort, playlistsToSortInto)
        for index, song in enumerate(songsToSort):
            clearCli()
            print(f"Song {index+1}/{len(songsToSort)}")
            playlistsToAddSongInto = askMultipleChoiceQuestion(f"Choose which playlists to add '{song.name}' to.", playlistsToSortIntoNamesToIds.keys())

            for playlist in playlistsToAddSongInto:
                print(f"Adding {song.name} into {playlist}...")
                self._addSongToPlaylist(playlistsToSortIntoNamesToIds[playlist], song.id)