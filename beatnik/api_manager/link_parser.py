import re

from urllib import parse

class LinkParser:
    apple_netloc = 'apple.com'
    soundcloud_netloc = 'soundcloud.com'
    spotify_netloc = 'open.spotify.com'
    tidal_netloc = 'tidal.com'
    ytm_netloc = 'music.youtube.com'

    soundcloud_album_prefix = 'sets'
    spotify_album_prefix = 'album'
    spotify_track_prefix = 'track'
    tidal_album_prefix = 'album'
    tidal_track_prefix = 'track'

    def __init__(self, apple_api, soundcloud_api, spotify_api, tidal_api, ytm_api):
        self.apple_api = apple_api
        self.soundcloud_api = soundcloud_api
        self.spotify_api = spotify_api
        self.tidal_api = tidal_api
        self.ytm_api = ytm_api

    def clean_title(self, title):
        regex = re.compile('( \- \d{4})?( \-[a-z\s]*remaster(ed)?| \(remaster(ed)?\))', re.IGNORECASE)
        return regex.sub('', title)

    def parse_apple_link(self, music):
        url = parse.urlparse(music.apple_url)
        if (url.query == ''):
            album_id = url.path.split('/')[-1]
            result = self.apple_api.get_album(album_id)['data'][0]
            music.music_type = 'A'
        else:
            track_id = parse.parse_qs(url.query)['i'][0]
            result = self.apple_api.get_track(track_id)['data'][0]
            music.music_type = 'T'
            music.album = result['attributes']['albumName']

        art = result['attributes']['artwork']
        music.name = result['attributes']['name']
        music.artist = result['attributes']['artistName']
        music.artwork = art['url'].format(w=art['width'], h=art['height'])

        return music

    def parse_soundcloud_link(self, music):
        url = parse.urlparse(music.soundcloud_url)
        result = self.soundcloud_api.get(music.soundcloud_url)
        if result['type'] == "album":
            music.music_type = 'A'
        else:
            music.music_type = 'T'

        music.name = result['title']
        music.artist = result['artist']
        music.artwork = result['art']

        return music

    def parse_spotify_link(self, music):
        url = parse.urlparse(music.spotify_url)
        item_id = url.path.split('/')[-1]
        prefix = url.path.split('/')[1]
        if prefix == self.spotify_album_prefix:
            result = self.spotify_api.album(item_id)
            music.music_type = 'A'
            music.artwork = result['images'][0]['url']
        elif prefix == self.spotify_track_prefix:
            result = self.spotify_api.track(item_id)
            music.music_type = 'T'
            music.album = result['album']['name']
            music.artwork = result['album']['images'][0]['url']

        music.name = self.clean_title(result['name'])
        music.artist = result['artists'][0]['name']

        return music

    def parse_tidal_link(self, music):
        url = parse.urlparse(music.tidal_url)
        path_segments = url.path.split('/')
        item_id = path_segments[-1]
        for segment in path_segments:
            if segment in [self.tidal_album_prefix, self.tidal_track_prefix]:
                prefix = segment

        if prefix == self.tidal_album_prefix:
            result = self.tidal_api.get_album(item_id)
            music.music_type = 'A'
        elif prefix == self.tidal_track_prefix:
            result = self.tidal_api.get_track_radio(item_id)[0]
            music.music_type = 'T'
            music.album = result.album.name

        music.name = self.clean_title(result.name)
        music.artist = result.artist.name

        return music

    def parse_ytm_link(self, music):
        url = parse.urlparse(music.ytm_url)
        query_params = parse.parse_qs(url.query)
        if 'list' in query_params:
            music.music_type = 'A'
            browse_id = self.ytm_api.get_album_browse_id(query_params['list'][0])
            if not browse_id:
                return music

            result = self.ytm_api.get_album(browse_id)
            music.artist = result["artist"][0]["name"]
        elif 'video' in query_params:
            music.music_type = 'T'
            result = self.ytm_api.get_song(query_params['video'][0])
            music.artist = result["artists"][0]

        music.name = self.clean_title(result["title"])

        return music

    def get_spotify_artwork(self, music):
        if music.spotify_url is None:
            return None

        url = parse.urlparse(music.spotify_url)
        item_id = url.path.split('/')[-1]
        prefix = url.path.split('/')[1]
        if prefix == self.spotify_album_prefix:
            result = self.spotify_api.album(item_id)
            return result['images'][0]['url']
        else:
            result = self.spotify_api.track(item_id)
            return result['album']['images'][0]['url']
