import re

class LinkParser:
    gpm_netloc = 'play.google.com'
    soundcloud_netloc = 'soundcloud.com'
    spotify_netloc = 'open.spotify.com'

    gpm_album_prefix = 'B'
    gpm_track_prefix = 'T'
    soundcloud_album_prefix = 'sets'
    spotify_album_prefix = 'album'
    spotify_track_prefix = 'track'

    def __init__(self, gpm_api, soundcloud_api, spotify_api):
        self.gpm_api = gpm_api
        self.soundcloud_api = soundcloud_api
        self.spotify_api = spotify_api

    def clean_title(self, title):
        regex = re.compile('( \- \d{4} )?\-?[a-z\s]*\(?remaster(ed)?\)?', re.IGNORECASE)
        return regex.sub('', title)

    def parse_gpm_link(self, url):
        item_id = url.path.split('/')[-1]
        prefix = item_id[:1]
        if prefix == self.gpm_album_prefix:
            album = self.gpm_api.get_album_info(item_id)
            info = {
                'type': "album",
                'title': album['name'],
                'artist': album['artist'],
                'art': album['albumArtRef']
            }
        elif prefix == self.gpm_track_prefix:
            track = self.gpm_api.get_track_info(item_id)
            info = {
                'type': "track",
                'title': track['title'],
                'artist': track['artist'],
                'art': track['albumArtRef'][0]['url'],
                'album': track['album']
            }
        return info 

    def parse_soundcloud_link(self, url):
        item = self.soundcloud_api.get('/resolve', url=url)
        info = {
            'type': item.type if item.kind == 'playlist' else item.kind,
            'title': item.title,
            'artist': item.user['username'],
            'art': item.artwork_url
        }
        
        return info

    def parse_spotify_link(self, url):
        item_id = url.path.split('/')[-1]
        prefix = url.path.split('/')[1] 
        if prefix == self.spotify_album_prefix:
            album = self.spotify_api.album(item_id)
            info = {
                'type': "album",
                'title': self.clean_title(album['name']),
                'artist': album['artists'][0]['name'],
                'art': album['images'][0]['url']
            }
        elif prefix == self.spotify_track_prefix:
            track = self.spotify_api.track(item_id)
            info = {
                'type': "track",
                'title': self.clean_title(track['name']),
                'artist': track['artists'][0]['name'],
                'art': track['album']['images'][0]['url'],
                'album': track['album']['name']
            }
        return info
