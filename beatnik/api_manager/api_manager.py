import logging
import os
import spotipy
import sys

from beatnik.api_manager.clients import AppleMusicApi, SoundcloudApi
from beatnik.api_manager.link_converter import LinkConverter
from beatnik.api_manager.link_parser import LinkParser
from beatnik.api_manager.search_handler import SearchHandler
from gmusicapi import Mobileclient
from spotipy.oauth2 import SpotifyClientCredentials
from tidalapi import Session

class ApiManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.apple_api = self.get_apple_api()
        self.gpm_api = self.get_gpm_api()
        self.soundcloud_api = self.get_soundcloud_api()
        self.spotify_api = self.get_spotify_api()
        self.tidal_api = self.get_tidal_api()
        self.link_parser = LinkParser(
                self.apple_api,
                self.gpm_api,
                self.soundcloud_api,
                self.spotify_api,
                self.tidal_api)
        self.link_converter = LinkConverter(
                self.apple_api,
                self.gpm_api,
                self.soundcloud_api,
                self.spotify_api,
                self.tidal_api,
                self.link_parser)
        self.search_handler = SearchHandler(self.spotify_api, self.link_converter)

    def get_apple_api(self):
        try:
            key_id = os.environ['APPLE_KEY_ID']
            issuer = os.environ['APPLE_KEY_ISSUER']
            key = os.environ['APPLE_KEY']
            return AppleMusicApi(key_id=key_id, issuer=issuer, key=key)
        except Exception as e:
            self.logger.error("Something went wrong getting Apple Music API")
            self.logger.error(e)
            return None

    def get_gpm_api(self):
        try:
            gpm_api = Mobileclient()
            username = os.environ['GPM_USERNAME']
            password = os.environ['GPM_PASSWORD']

            if (not gpm_api.login(username, password, Mobileclient.FROM_MAC_ADDRESS, 'en_US')):
                self.logger.error("Unable to login to Google Play Music.")
                return None

            return gpm_api
        except Exception as e:
            self.logger.error("Something went wrong getting Google Play Music API")
            self.logger.error(e)
            return None

    def get_soundcloud_api(self):
        try:
            return SoundcloudApi()
        except Exception as e:
            self.logger.error("Something went wrong getting Soundcloud API")
            self.logger.error(e)
            return None

    def get_spotify_api(self):
        try:
            client_credentials_manager = SpotifyClientCredentials()
            return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        except Exception as e:
            self.logger.error("Something went wrong getting Spotify API")
            self.logger.error(e)
            return None

    def get_tidal_api(self):
        try:
            session = Session()
            username = os.environ['TIDAL_USERNAME']
            password = os.environ['TIDAL_PASSWORD']

            if (not session.login(username, password)):
                self.logger.error("Unable to login to Tidal")
                return None

            return session
        except Exception as e:
            self.logger.error("Something went wrong getting Tidal API")
            self.logger.error(e)
            return None

    def convert_link(self, music):
        music = self.link_converter.convert_link(music)

        return music
