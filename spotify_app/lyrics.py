
import requests
from bs4 import BeautifulSoup
from .models import track_object,artist_object_new as artist_object
from .api_spotify_wrapper import Spotify
class Lyrics():

    def __init__(self):

        self.lyricheaders = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def get_lyrics(self,query):
        self.lyrics = ''
        s = requests.Session()
        url = 'https://www.google.com/search?q={}&ie=utf-8&oe=utf-8'.format(query)
        r = s.get(url, headers=self.lyricheaders)
        soup = BeautifulSoup(r.text, "html.parser").find_all("span", {"jsname": "YS01Ge"})
        for link in soup:
            self.lyrics += (link.text + '<br>')
        return  self.lyrics

