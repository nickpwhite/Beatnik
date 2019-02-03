import re

from urllib import parse

class LinkParser:
    apple_netloc = 'itunes.apple.com'
    gpm_netloc = 'google.com'
    soundcloud_netloc = 'soundcloud.com'
    spotify_netloc = 'open.spotify.com'

    gpm_album_prefix = 'B'
    gpm_track_prefix = 'T'
    soundcloud_album_prefix = 'sets'
    spotify_album_prefix = 'album'
    spotify_track_prefix = 'track'

    def __init__(self, apple_api, gpm_api, soundcloud_api, spotify_api):
        self.apple_api = apple_api
        self.gpm_api = gpm_api
        self.soundcloud_api = soundcloud_api
        self.spotify_api = spotify_api

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

    def parse_gpm_link(self, music):
        if self.gpm_api is None:
            return {}

        url = parse.urlparse(music.gpm_url)
        item_id = url.path.split('/')[-1]
        prefix = item_id[:1]
        if prefix == self.gpm_album_prefix:
            result = self.gpm_api.get_album_info(item_id)
            music.music_type = 'A'
            music.name = self.clean_title(result['name'])
            music.artwork = result['albumArtRef'].replace('http:', 'https:', 1)
        elif prefix == self.gpm_track_prefix:
            result = self.gpm_api.get_track_info(item_id)
            music.music_type = 'T'
            music.album = result['album']
            music.name = self.clean_title(result['title'])
            music.artwork = result['albumArtRef'][0]['url'].replace('http:', 'https:', 1),

        music.artist = result['artist']

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

    def get_spotify_artwork(self, music):
        url = parse.urlparse(music.spotify_url)
        item_id = url.path.split('/')[-1]
        prefix = url.path.split('/')[1]
        if prefix == self.spotify_album_prefix:
            result = self.spotify_api.album(item_id)
            return result['images'][0]['url']
        else:
            result = self.spotify_api.track(item_id)
            return result['album']['images'][0]['url']
