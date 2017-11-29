import os
import soundcloud
import spotipy
import sys

from gmusicapi import Mobileclient
from spotipy.oauth2 import SpotifyClientCredentials
from urllib import parse

from . import LinkParser

class LinkConverter:
    gpm_format = "https://play.google.com/music/m/{0}"

    def __init__(self):
        self.gpm_api = self.get_gpm_api()
        self.soundcloud_api = self.get_soundcloud_api()
        self.spotify_api = self.get_spotify_api()
        self.link_parser = LinkParser.LinkParser(self.gpm_api, self.soundcloud_api, self.spotify_api)

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

        return soundcloud.Client(
                client_id=client_id,
                client_secret=client_secret,
                username=username,
                password=password)

    def get_spotify_api(self):
        client_credentials_manager = SpotifyClientCredentials()
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def convert_link(self, link):
        url = parse.urlparse(link)
        if self.link_parser.gpm_netloc in url.netloc:
            info = self.link_parser.parse_gpm_link(url)
        elif self.link_parser.soundcloud_netloc in url.netloc:
            info = self.link_parser.parse_soundcloud_link(link)
        elif self.link_parser.spotify_netloc in url.netloc:
            info = self.link_parser.parse_spotify_link(url)
        else:
            raise ValueError("Received a link I can't handle: {0}".format(link))

        if info[0] == "track":
            gpm_link = self.get_gpm_track(info[1:])
            soundcloud_link = self.get_soundcloud_track(info[1:])
            spotify_link = self.get_spotify_track(info[1:])
            links = { 'gpm_link': gpm_link, 'soundcloud_link': soundcloud_link, 'spotify_link': spotify_link }
        elif info[0] == "album":
            gpm_link = self.get_gpm_album(info[1:])
            soundcloud_link = self.get_soundcloud_album(info[1:])
            spotify_link = self.get_spotify_album(info[1:])
            links = { 'gpm_link': gpm_link, 'soundcloud_link': soundcloud_link, 'spotify_link': spotify_link }
        else:
            raise ValueError("Received a media type I can't handle: {0}".format(info))

        return links

    def get_gpm_album(self, album_info):
        query = "{0} {1}".format(album_info[0], album_info[1])
        results = self.gpm_api.search(query, max_results = 1)
        if (len(results['album_hits']) > 0):
            album_id = results['album_hits'][0]['album']['albumId']
            return self.gpm_format.format(album_id)
        else:
            print("Could not find an album on Google Play using the following info:\n{0}".format(album_info))
            return None

    def get_gpm_track(self, track_info):
        query = "\"{0}\" \"{1}\"".format(track_info[0], track_info[1])
        results = self.gpm_api.search(query, max_results = 1)
        if (len(results['song_hits']) > 0):
            track_id = "T{0}".format(results['song_hits'][0]['track']['nid'])
            return self.gpm_format.format(track_id)
        else:
            print("Could not find a track on Google Play using the following info:\n{0}".format(track_info))
            return None

    def get_soundcloud_album(self, album_info):
        query = "{0} {1}".format(album_info[0], album_info[1])
        results = self.soundcloud_api.get('/playlists', q=query)
        for album in results:
            if (album.title == album_info[0] and album.user['username'] == album_info[1]):
                return album.permalink_url
        print("Could not find an album on Soundcloud using the following info:\n{0}".format(album_info))
        return None

    def get_soundcloud_track(self, track_info):
        query = "{0} {1}".format(track_info[0], track_info[1])
        results = self.soundcloud_api.get('/tracks', q=query)
        for track in results:
            if (track.user['username'] == track_info[1]):
                return track.permalink_url
        print("Could not find an track on Soundcloud using the following info:\n{0}".format(track_info))
        return None

    def get_spotify_album(self, album_info):
        query = "album:{0} artist:{1}".format(album_info[0], album_info[1])
        results = self.spotify_api.search(query, limit = 10, type = "album")
        if (results['albums']['total'] > 0):
            return results['albums']['items'][0]['external_urls']['spotify']
        else:
            print("Could not find an album on Spotify using the following info:\n{0}".format(album_info))
            return None

    def get_spotify_track(self, track_info):
        query = "track:{0} artist:{1}".format(track_info[0], track_info[1])
        results = self.spotify_api.search(query, limit = 10, type = "track")
        if (results['tracks']['total'] > 0):
            return results['tracks']['items'][0]['external_urls']['spotify']
        else:
            print("Could not find a track on Spotify using the following info:\n{0}".format(track_info))
            return None
