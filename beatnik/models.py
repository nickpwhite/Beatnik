from django.db import models

class Music(models.Model):
    music_type = models.CharField("Album or Track", max_length = 1, choices=(('A', 'Album'), ('T', 'Track')))
    name = models.CharField("Track Name", max_length = 200)
    artist = models.CharField("Artist Name", max_length = 200)
    album = models.CharField("Album Name", max_length = 200, blank = True)
    apple_url = models.URLField("Apple Music URL")
    gpm_url = models.URLField("Google Play Music URL")
    soundcloud_url = models.URLField("Soundcloud URL")
    spotify_url = models.URLField("Spotify URL")
    match_rating = models.IntegerField("Rating of the match", default=0)
    artwork = models.URLField("Album art URL")

    def __init__(
            self,
            music_type,
            name,
            artist,
            album,
            apple_url,
            gpm_url,
            soundcloud_url,
            spotify_url,
            artwork):
        self.music_type = music_type
        self.name = name
        self.artist = artist
        self.album = album
        self.apple_url = apple_url
        self.gpm_url = gpm_url
        self.soundcloud_url = soundcloud_url
        self.spotify_url = spotify_url
        self.artwork = artwork
