from spotipy import Spotify
from spotipy.util import prompt_for_user_token

from CONSTS import SpotifySessionConsts


class SpotifySession:
    def __init__(self, username: str):
        self.consts = SpotifySessionConsts()
        token = prompt_for_user_token(username=username, 
                                      scope=self.consts.SCOPE, 
                                      client_id=self.consts.ID, 
                                      client_secret=self.consts.SECRET, 
                                      redirect_uri=self.consts.URL)
        
        self.spotify = Spotify(token)