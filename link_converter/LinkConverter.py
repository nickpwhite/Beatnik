import os
import soundcloud
import spotipy
import sys

from gmusicapi import Mobileclient
from spotipy.oauth2 import SpotifyClientCredentials
from urllib import parse

from . import LinkParser
from apple_music_api import AppleMusicApi

class LinkConverter:
    gpm_format = "https://play.google.com/music/m/{0}"

    def __init__(self):
        self.apple_api = self.get_apple_api()
        self.gpm_api = self.get_gpm_api()
        self.soundcloud_api = self.get_soundcloud_api()
        self.spotify_api = self.get_spotify_api()
        self.link_parser = LinkParser.LinkParser(self.apple_api, self.gpm_api, self.soundcloud_api, self.spotify_api)

    def get_apple_api(self):
        key_id = os.environ['APPLE_KEY_ID']
        issuer = os.environ['APPLE_KEY_ISSUER']
        key = os.environ['APPLE_KEY']
        return AppleMusicApi.AppleMusicApi(key_id=key_id,
                issuer=issuer,
                key=key)
        
    def get_gpm_api(self):
        gpm_api = Mobileclient()
        username = os.environ['GPM_USERNAME']
        password = os.environ['GPM_PASSWORD']

        if (not gpm_api.login(username, password, Mobileclient.FROM_MAC_ADDRESS, 'en_US')):
            print("Unable to login to Google Play Music.")
            sys.exit(-1)

        return gpm_api

    def get_soundcloud_api(self):
        client_id = os.environ['SOUNDCLOUD_CLIENT_ID']
        client_secret = os.environ['SOUNDCLOUD_CLIENT_SECRET']
        username = os.environ['SOUNDCLOUD_USERNAME']
        password = os.environ['SOUNDCLOUD_PASSWORD']

        try:
            client = soundcloud.Client(
                    client_id=client_id,
                    client_secret=client_secret,
                    username=username,
                    password=password)
            return client
        except BaseException as e:
            print("Unable to login to Soundcloud with exception {0}".format(e))
            return None


    def get_spotify_api(self):
        client_credentials_manager = SpotifyClientCredentials()
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def convert_link(self, link):
        url = parse.urlparse(link)
        if self.link_parser.apple_netloc in url.netloc:
            info = self.link_parser.parse_apple_link(url)
        elif self.link_parser.gpm_netloc in url.netloc:
            info = self.link_parser.parse_gpm_link(url)
        elif self.link_parser.soundcloud_netloc in url.netloc:
            info = self.link_parser.parse_soundcloud_link(link)
        elif self.link_parser.spotify_netloc in url.netloc:
            info = self.link_parser.parse_spotify_link(url)
        else:
            raise ValueError("Received a link I can't handle: {0}".format(link))

        if info['type'] == "track":
            apple_link = self.get_apple_track(info)
            gpm_link = self.get_gpm_track(info)
            soundcloud_link = self.get_soundcloud_track(info)
            spotify_link = self.get_spotify_track(info)
        elif info['type'] == "album":
            apple_link = self.get_apple_album(info)
            gpm_link = self.get_gpm_album(info)
            soundcloud_link = self.get_soundcloud_album(info)
            spotify_link = self.get_spotify_album(info)
        else:
            raise ValueError("Received a media type I can't handle: {0}".format(info))

        info['links'] = {
            'apple_link': apple_link,
            'gpm_link': gpm_link,
            'soundcloud_link': soundcloud_link,
            'spotify_link': spotify_link
        }
        return info

    def get_apple_album(self, album_info):
        query = "{0} {1}".format(album_info['title'], album_info['artist'])
        results = self.apple_api.search(query, limit = 1, types='albums')
        if (results is not None):
            album = results['albums']['data'][0]
            return album['attributes']['url']
        else:
            return None

    def get_apple_track(self, track_info):
        query = "{0} {1}".format(track_info['title'], track_info['artist'])
        results = self.apple_api.search(query, limit = 1, types='songs')
        if (results is not None):
            track = results['songs']['data'][0]
            return track['attributes']['url']
        else:
            return None

    def get_gpm_album(self, album_info):
        query = "{0} {1}".format(album_info['title'], album_info['artist'])
        results = self.gpm_api.search(query, max_results = 1)
        if (len(results['album_hits']) > 0):
            album_id = results['album_hits'][0]['album']['albumId']
            return self.gpm_format.format(album_id)
        else:
            return None

    def get_gpm_track(self, track_info):
        query = "\"{0}\" \"{1}\"".format(track_info['title'], track_info['artist'])
        results = self.gpm_api.search(query, max_results = 1)
        if (len(results['song_hits']) > 0):
            track_id = "T{0}".format(results['song_hits'][0]['track']['nid'])
            return self.gpm_format.format(track_id)
        else:
            return None

    def get_soundcloud_album(self, album_info):
        query = "{0} {1}".format(album_info['title'], album_info['artist'])
        results = self.soundcloud_api.get('/playlists', q=query)
        for album in results:
            if (album.title == album_info['title'] and album.user['username'] == album_info['artist']):
                return album.permalink_url
        return None

    def get_soundcloud_track(self, track_info):
        query = "{0} {1}".format(track_info['title'], track_info['artist'])
        results = self.soundcloud_api.get('/tracks', q=query)
        for track in results:
            if (track.user['username'] == track_info['artist']):
                return track.permalink_url
        return None

    def get_spotify_album(self, album_info):
        query = "album:{0} artist:{1}".format(album_info['title'], album_info['artist'])
        results = self.spotify_api.search(query, limit = 10, type = "album")
        if (results['albums']['total'] > 0):
            return results['albums']['items'][0]['external_urls']['spotify']
        else:
            return None

    def get_spotify_track(self, track_info):
        query = "track:{0} artist:{1}".format(track_info['title'], track_info['artist'])
        results = self.spotify_api.search(query, limit = 10, type = "track")
        if (results['tracks']['total'] > 0):
            return results['tracks']['items'][0]['external_urls']['spotify']
        else:
            return None
