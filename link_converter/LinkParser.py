class LinkParser:
    gpm_netloc = 'play.google.com'
    spotify_netloc = 'open.spotify.com'

    gpm_album_prefix = 'B'
    gpm_track_prefix = 'T'
    spotify_album_prefix = 'album'
    spotify_track_prefix = 'track'

    def __init__(self, gpm_api, spotify_api):
        self.gpm_api = gpm_api
        self.spotify_api = spotify_api

    def parse_gpm_link(self, url):
        # item could be either a track or an album
        item_id = url.path.split('/')[-1]
        prefix = item_id[:1]
        if prefix == self.gpm_album_prefix:
            album = self.gpm_api.get_album_info(item_id)
            return ("album", album['name'], album['artist'])
        elif prefix == self.gpm_track_prefix:
            track = self.gpm_api.get_track_info(item_id)
            return ("track", track['title'], track['artist'])

    def parse_spotify_link(self, url):
        # item could be either a track or an album
        item_id = url.path.split('/')[-1]
        prefix = url.path.split('/')[1] 
        if prefix == self.spotify_album_prefix:
            album = self.spotify_api.album(item_id)
            return ("album", album['name'], album['artists'][0]['name'])
        elif prefix == self.spotify_track_prefix:
            track = self.spotify_api.track(item_id)
            return ("track", track['name'], track['artists'][0]['name'])
