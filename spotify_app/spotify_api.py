
import logging
import requests
from datetime import datetime
from django.contrib.auth.models import User
from .models import user_object,external_urls \
    ,playlist_object,track_object,external_ids,album_object,image_object, artist_object_new as artist_object,followers_object, currently_playing_object,context_object,user_track_history
from spotify_app.api_spotify_wrapper import Spotify
from .lyrics import Lyrics
def create_logger():
    logger = logging.getLogger('test')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

class SpotifyApi():
    def __init__(self, user_object):
        self.auth_token = user_object.extra_data['access_token']
        self.refresh_token = user_object.extra_data['access_token']
        self.user_id = user_object.user_id
        self.user = self.current_user()

    def current_user(self):
        data = Spotify(auth=self.auth_token).current_user()
        user = self._user_parser(data)
        return user

    def next_track(self):
        datas = Spotify(auth=self.auth_token).next_track(self._device_parser())


    def get_user_playlists(self):
        ##Playlist success
        datas = Spotify(auth=self.auth_token).user_playlist(self.user.id)

        for data in datas["items"]:
            t = self._simple_playlist_parser(data)
        print('success get_user_playlists')

    def user_track_history(self):
        '''
        https://developer.spotify.com/documentation/web-api/reference/player/get-recently-played/
        :return: list of play history objects
        '''
        datas = Spotify(auth=self.auth_token).current_user_recently_played()

        for data in datas["items"]:
                track = self._simple_track_parser(data['track'])
                user_track_history(user = self.user,played_at = data['played_at'],track = track).save()

    def get_user_currently_playing(self):
        datas = Spotify(auth=self.auth_token).current_user_playing_track()


        if datas:
            return self._currently_playing_parser(datas)

    def _device_parser(self,name=None):
        datas = Spotify(auth=self.auth_token).devices()
        print(datas)
        if name:
            for data in datas['devices']:
                if data['is_active'] and data['name']=='Web Playback SDK Quick Start Player':
                    return data['id']
                else:
                    pass
        else:
            for data in datas['devices']:
                if data['is_active'] and data['type']=='Smartphone':
                    return data['id']
                else:
                    pass

    def _simple_context_parser(self,data):
        if data:
            context = context_object(
            type= data['type'],
            href = data['href'],
            external_urls = external_urls(json=data['external_urls']),
            uri = data['uri'],
            )
            return context
        else:
            return None

    def prepare_track(self, track_id, artist_id):

        if track_object.objects.filter(id=track_id).exists():
            track = track_object.objects.get(id=track_id)
        else:
            datas = Spotify(auth=self.auth_token).track(track_id)
            self._simple_track_parser(datas)
            track = track_object.objects.get(id=track_id)

        if artist_object.objects.filter(id=artist_id).exists():
            artist = artist_object.objects.get(id=artist_id)
        else:
            datas = Spotify(auth=self.auth_token).artist(artist_id)
            self._simle_artist_parser(datas)
            artist = artist_object.objects.get(id=artist_id)

        query = (str(track.name) + '+' + str(artist.name) + '+lyrics').replace(' ', '+')
        lyrics = Lyrics().get_lyrics(query)
        return lyrics

    def _currently_playing_parser(self, data):

        currently_playing = currently_playing_object(
            context= self._simple_context_parser(data['context']),
            user = self.user,
            timestamp = datetime.fromtimestamp(float(data["timestamp"]) / 1000),
            progress_ms = data['progress_ms'],
            is_playing = data['is_playing'],
            track = data['item']['id'],
            currently_playing_type=data['currently_playing_type']
        )
        currently_playing.save()

        return currently_playing


    def _user_parser(self,data):
        user = user_object(
            display_name=data['display_name'],
            external_urls = external_urls(json=data['external_urls']),
            followers = followers_object(), ##
            href = data['href'],
            id = data['id'],
            images=image_object(images=data['images']),
            type=data['type'],
            uri=data['uri'],
        )
        return user

    def _simple_track_parser(self, data):
        artist = [self._simle_artist_parser(artists).id for artists in data['artists']]
        album = self._simle_album_parser(data)
        track = track_object(
            artist = artist,
            album = album,
            #available_markets = data['available_markets'],
            disc_number=data['disc_number'],
            duration_ms=data['duration_ms'],
            explicit=data['explicit'],
            external_urls = external_urls(json=data['external_urls']),
            external_ids=external_ids(json=data['external_ids']),
            href=data['href'],
            id=data['id'],
            #is_playable = data['tracks']['is_playable'],
            #linked_from = linked_track_object(external_urls=data['external_urls'](json=data['linked_from'])),
            name=data['name'],
            preview_url=data['preview_url'],
            track_number=data['track_number'],
            type=data['type'],
            uri=data['uri'],
        )
        track.save()
        return track

    def _simle_album_parser(self,data):
        artist = [self._simle_artist_parser(artists).id for artists in data['album']['artists']]

        album = album_object(
            album_group=data['album']['album_group'] if 'album_group' in data['album'] else None,
            album_type=data['album']['album_type'],
            artist= artist,
            external_urls=external_urls(json=data['album']['external_urls']),
            href=data['album']['href'],
            id=data['album']['id'],
            images=image_object(images = data['album']['images']),
            name=data['album']['name'],
            release_date=data['album']['release_date'],
            release_date_precision=data['album']['release_date_precision'],
            type=data['album']['type'],
            uri=data['album']['uri'],
        )
        return album

    def _simle_artist_parser(self,artist_data):
        artist = artist_object(
            external_urls=external_urls(json=artist_data['external_urls']),
            href=artist_data['href'],
            id=artist_data['id'],
            name=artist_data['name'],
            type=artist_data['type'],
            uri=artist_data['uri']
        )
        artist.save()
        return artist

    def _simple_playlist_parser(self,playlist_data):
        playlist = playlist_object(
            collaborative= playlist_data['collaborative'],
            external_urls=external_urls(json=playlist_data['external_urls']),
            href=playlist_data['href'],
            id=playlist_data['id'],
            images=image_object(images=playlist_data['images']),
            name=playlist_data['name'],
            tracks = playlist_data['tracks']['href'],
            owner=self.user,
            public=playlist_data['public'],
            snapshot_id=playlist_data['snapshot_id'],
            type=playlist_data['type'],
            uri=playlist_data['uri']
        )
        playlist.save()
        return playlist

class SpotifyRefreshUsers():
    """
    Scheduled refresh token to keep all users conenction alive
    """
    def __init__(self):
        self.users = User.objects.all()
        self.refresh_token_url = "https://accounts.spotify.com/api/token"
        self.payload = "grant_type=refresh_token&refresh_token="
        self.headers = {'Content-Type': "application/x-www-form-urlencoded",
                        'Authorization': "Basic YTlhODIwM2U2OTdhNDE0MTgyNTNkOTgyMGE4OWYwY2U6MzcxYjM5NTg3ZWJjNDg1NWIzNGE1ZjM2YzdlMjJlZDY=", }

        self.querystring = {"grant_type": "refresh_token",
                            "refresh_token": ""}

    def refresh_token(self):
        '''
        TO BE CLEANED
        :return:
        '''
        for user in self.users:
            user = User.objects.get(username=user)
            try:
                social = user.social_auth.get(provider='spotify')
                refresh_token = social.extra_data['refresh_token']
                self.querystring["refresh_token"]= refresh_token
                self.payload = self.payload + refresh_token
                response = requests.request("POST", self.refresh_token_url, data=self.payload, headers=self.headers, params=self.querystring)
                social.extra_data['access_token'] = response.json()['access_token']
                social.save()
            except Exception as e:
                print(str(e))



