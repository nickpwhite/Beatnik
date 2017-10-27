#!/usr/bin/python3

import getpass
import spotipy

from gmusicapi import Mobileclient
from spotipy.oauth2 import SpotifyClientCredentials
from urllib import parse

class LinkConverter:
    gpm_netloc = 'play.google.com'
    spotify_netloc = 'open.spotify.com'
    apple_netloc = 'itunes.apple.com'

    gpm_format = "https://play.google.com/music/m/{0}"

    def __init__(self):
        self.gpm_api = self.get_gpm_api()
        self.spotify_api = self.get_spotify_api()

    def get_gpm_api(self):
        gpm_api = Mobileclient()
        username = input("Enter your Google Play Music email address: ")
        password = getpass.getpass("Enter your password: ")

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
        gpm_link = parse.urlunparse(url) 
        song_info = url.query.replace("t=", '').replace('_', ' ').split(" - ")
        spotify_link = self.get_spotify_link(song_info)
        return (gpm_link, spotify_link)

    def parse_spotify_link(self, url):
        spotify_link = parse.urlunparse(url)
        track_id = url.path.split('/')[2]
        track = self.spotify_api.track(track_id)
        song_info = (track['artists'][0]['name'], track['name'])
        gpm_link = self.get_gpm_link(song_info)
        return (gpm_link, spotify_link)

    def get_gpm_link(self, song_info):
        query = "{0} - {1}".format(song_info[0], song_info[1])
        results = self.gpm_api.search(query, max_results = 1)
        if (len(results['song_hits']) > 0):
            track_id = "T{0}".format(results['song_hits'][0]['track']['nid'])
            return self.gpm_format.format(track_id)
        else:
            print("Could not find a track on Google Play using the following info:\n{0}".format(song_info))
            return None

    def get_spotify_link(self, song_info):
        query = "track:{0} artist:{1}".format(song_info[0], song_info[1])
        results = self.spotify_api.search(query, limit = 10, type = "track")
        if (results['tracks']['total'] > 0):
            return results['tracks']['items'][0]['external_urls']['spotify']
        else:
            print("Could not find a track on Spotify using the following info:\n{0}".format(song_info))
            return None
