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
            self.logger.error("Received a link I can't handle: {0}".format(link))

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
            self.logger.error("Received a media type I can't handle: {0}".format(info))

        info['links'] = {
            'apple_link': apple_link,
            'gpm_link': gpm_link,
            'soundcloud_link': soundcloud_link,
            'spotify_link': spotify_link
        }
        return info

    def get_apple_link(self, info):
        if info['type'] == 'album':
            return self.get_apple_album(info)
        elif info['type'] == 'track':
            return self.get_apple_track(info)
        else:
            self.logger.warning("Encountered unknown type: {0}".format(info['type']))

    def get_apple_album(self, album_info):
        query = "{0} {1}".format(album_info['title'], album_info['artist'])
        results = self.apple_api.search(query, limit = 1, types='albums')
        if (results != {}):
            album = results['albums']['data'][0]
            return album['attributes']['url']
        else:
            return None

    def get_apple_track(self, track_info):
        query = "{0} {1}".format(track_info['title'], track_info['artist'])
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

    def get_gpm_album(self, album_info):
        query = "{0} {1}".format(album_info['title'], album_info['artist'])
        results = self.gpm_api.search(query, max_results = 1)
        if (len(results['album_hits']) > 0):
            album_id = results['album_hits'][0]['album']['albumId']
            return self.gpm_format.format(album_id)
        else:
            return None

    def get_gpm_track(self, track_info):
        query = "{0} {1}".format(track_info['title'], self.sanitize(track_info['artist']))
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

    def get_soundcloud_album(self, album_info):
        return self.soundcloud_api.search(album_info['title'], album_info['artist'])

    def get_soundcloud_track(self, track_info):
        return self.soundcloud_api.search(track_info['title'], track_info['artist'])

    def get_spotify_link(self, info):
        if info['type'] == 'album':
            return self.get_spotify_album(info)
        elif info['type'] == 'track':
            return self.get_spotify_track(info)
        else:
            self.logger.warning("Encountered unknown type: {0}".format(info['type']))

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

    def sanitize(self, s):
        return s.replace(" & ", " ")
