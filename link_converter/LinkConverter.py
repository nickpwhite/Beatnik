#!/usr/bin/python3

import os
import spotipy
import sys

from gmusicapi import Mobileclient
from spotipy.oauth2 import SpotifyClientCredentials
from urllib import parse

class LinkConverter:
    gpm_netloc = 'play.google.com'
    spotify_netloc = 'open.spotify.com'
    apple_netloc = 'itunes.apple.com'

    gpm_format = "https://play.google.com/music/m/{0}"

    gpm_album_prefix = 'B'
    gpm_track_prefix = 'T'
    spotify_album_prefix = 'album'
    spotify_track_prefix = 'track'

    def __init__(self):
        self.gpm_api = self.get_gpm_api()
        self.spotify_api = self.get_spotify_api()

    def get_gpm_api(self):
        gpm_api = Mobileclient()
        username = os.environ['GPM_USERNAME']
        password = os.environ['GPM_PASSWORD']

        if (not gpm_api.login(username, password, Mobileclient.FROM_MAC_ADDRESS, 'en_US')):
            print("Unable to login to Google Play Music.")
            sys.exit(-1)

        return gpm_api

    def get_spotify_api(self):
        client_credentials_manager = SpotifyClientCredentials()
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def convert_link(self, link):
        url = parse.urlparse(link)
        if self.gpm_netloc in url.netloc:
            return self.parse_gpm_link(url)
        elif self.spotify_netloc in url.netloc:
            return self.parse_spotify_link(url)
        elif self.apple_netloc in url.netloc:
            return self.parse_apple_link(url)
        else:
            raise ValueError("Received a link I can't handle: {0}".format(link))

    def parse_gpm_link(self, url):
        # item could be either a track or an album
        item_id = url.path.split('/')[-1]
        gpm_link = '{0}://{1}{2}'.format(url.scheme, url.netloc, url.path)
        prefix = item_id[:1]
        if prefix == self.gpm_album_prefix:
            album = self.gpm_api.get_album_info(item_id)
            album_info = (album['name'], album['artist'])
            spotify_link = self.get_spotify_album(album_info)
        elif prefix == self.gpm_track_prefix:
            track = self.gpm_api.get_track_info(item_id)
            track_info = (track['title'], track['artist'])
            spotify_link = self.get_spotify_track(track_info)
        return (gpm_link, spotify_link)

    def parse_spotify_link(self, url):
        # item could be either a track or an album
        item_id = url.path.split('/')[-1]
        spotify_link = parse.urlunparse(url)
        prefix = url.path.split('/')[1] 
        if prefix == self.spotify_album_prefix:
            album = self.spotify_api.album(item_id)
            album_info = (album['name'], album['artists'][0]['name'])
            gpm_link = self.get_gpm_album(album_info)
        elif prefix == self.spotify_track_prefix:
            track = self.spotify_api.track(item_id)
            track_info = (track['name'], track['artists'][0]['name'])
            gpm_link = self.get_gpm_track(track_info)
        return (gpm_link, spotify_link)

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
        query = "song:{0} {1}".format(track_info[0], track_info[1])
        results = self.gpm_api.search(query, max_results = 1)
        if (len(results['song_hits']) > 0):
            track_id = "T{0}".format(results['song_hits'][0]['track']['nid'])
            return self.gpm_format.format(track_id)
        else:
            print("Could not find a track on Google Play using the following info:\n{0}".format(track_info))
            return None

    def get_spotify_album(self, album_info):
        query = "album:{0} artist:{1}".format(album_info[0], track_info[1])
        results = self.spotify_api.search(query, limit = 10, type = "album")
        print(results)

    def get_spotify_track(self, track_info):
        query = "track:{0} artist:{1}".format(track_info[0], track_info[1])
        results = self.spotify_api.search(query, limit = 10, type = "track")
        if (results['tracks']['total'] > 0):
            return results['tracks']['items'][0]['external_urls']['spotify']
        else:
            print("Could not find a track on Spotify using the following info:\n{0}".format(track_info))
            return None
