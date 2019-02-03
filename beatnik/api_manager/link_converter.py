import logging

from urllib import parse

class LinkConverter:
    gpm_format = "https://music.google.com/music/m/{0}"

    def __init__(self, apple_api, gpm_api, soundcloud_api, spotify_api, link_parser):
        self.logger = logging.getLogger(__name__)
        self.apple_api = apple_api
        self.gpm_api = gpm_api
        self.soundcloud_api = soundcloud_api
        self.spotify_api = spotify_api
        self.link_parser = link_parser

    def convert_link(self, music):
        if music.apple_url is not None:
            music = self.link_parser.parse_apple_link(music)
        elif music.gpm_url is not None:
            music = self.link_parser.parse_gpm_link(music)
        elif music.soundcloud_url is not None:
            music = self.link_parser.parse_soundcloud_link(music)
        elif music.spotify_url is not None:
            music = self.link_parser.parse_spotify_link(music)
        else:
            self.logger.error("All the links were None")
            return music

        if music.music_type == 'T':
            music.apple_url = self.get_apple_track(music)
            music.gpm_url = self.get_gpm_track(music)
            music.soundcloud_url = self.get_soundcloud_track(music)
            music.spotify_url = self.get_spotify_track(music)
        elif music.music_type == 'A':
            music.apple_url = self.get_apple_album(music)
            music.gpm_url = self.get_gpm_album(music)
            music.soundcloud_url = self.get_soundcloud_album(music)
            music.spotify_url = self.get_spotify_album(music)
        else:
            self.logger.error("Received a media type I can't handle")

        return music

    def get_apple_link(self, info):
        if info['type'] == 'album':
            return self.get_apple_album(info)
        elif info['type'] == 'track':
            return self.get_apple_track(info)
        else:
            self.logger.warning("Encountered unknown type: {0}".format(info['type']))

    def get_apple_album(self, music):
        if music.apple_url is not None:
            return music.apple_url

        query = "{0} {1}".format(music.name, music.artist)
        results = self.apple_api.search(query, limit = 1, types='albums')
        if (results != {}):
            album = results['albums']['data'][0]
            return album['attributes']['url']
        else:
            return None

    def get_apple_track(self, music):
        if music.apple_url is not None:
            return music.apple_url

        query = "{0} {1}".format(music.name, music.artist)
        results = self.apple_api.search(query, limit = 1, types='songs')
        if (results != {}):
            track = results['songs']['data'][0]
            return track['attributes']['url']
        else:
            return None

    def get_gpm_link(self, info):
        if info['type'] == 'album':
            return self.get_gpm_album(info)
        elif info['type'] == 'track':
            return self.get_gpm_track(info)
        else:
            self.logger.warning("Encountered unknown type: {0}".format(info['type']))

    def get_gpm_album(self, music):
        if music.gpm_url is not None:
            return music.gpm_url

        if self.gpm_api is None:
            return None

        query = "{0} {1}".format(music.name, music.artist)
        results = self.gpm_api.search(query, max_results = 1)
        if (len(results['album_hits']) > 0):
            album_id = results['album_hits'][0]['album']['albumId']
            return self.gpm_format.format(album_id)
        else:
            return None

    def get_gpm_track(self, music):
        if music.gpm_url is not None:
            return music.gpm_url

        if self.gpm_api is None:
            return None

        query = "{0} {1}".format(music.name, self.sanitize(music.artist))
        results = self.gpm_api.search(query)
        if (len(results['song_hits']) > 0):
            track_id = "T{0}".format(results['song_hits'][0]['track']['nid'])
            return self.gpm_format.format(track_id)
        else:
            return None

    def get_soundcloud_link(self, info):
        if info['type'] == 'album':
            return self.get_soundcloud_album(info)
        elif info['type'] == 'track':
            return self.get_soundcloud_track(info)
        else:
            self.logger.warning("Encountered unknown type: {0}".format(info['type']))

    def get_soundcloud_album(self, music):
        if music.soundcloud_url is not None:
            return music.soundcloud_url

        return self.soundcloud_api.search(music.name, music.artist)

    def get_soundcloud_track(self, music):
        if music.soundcloud_url is not None:
            return music.soundcloud_url

        return self.soundcloud_api.search(music.name, music.artist)

    def get_spotify_link(self, info):
        if info['type'] == 'album':
            return self.get_spotify_album(info)
        elif info['type'] == 'track':
            return self.get_spotify_track(info)
        else:
            self.logger.warning("Encountered unknown type: {0}".format(info['type']))

    def get_spotify_album(self, music):
        if music.spotify_url is not None:
            return music.spotify_url

        query = "album:{0} artist:{1}".format(music.name, music.artist)
        results = self.spotify_api.search(query, limit = 10, type = "album")
        if (results['albums']['total'] > 0):
            return results['albums']['items'][0]['external_urls']['spotify']
        else:
            return None

    def get_spotify_track(self, music):
        if music.spotify_url is not None:
            return music.spotify_url

        query = "track:{0} artist:{1}".format(music.name, music.artist)
        results = self.spotify_api.search(query, limit = 10, type = "track")
        if (results['tracks']['total'] > 0):
            return results['tracks']['items'][0]['external_urls']['spotify']
        else:
            return None

    def sanitize(self, s):
        return s.replace(" & ", " ")
