from django.db.models import Model, CharField, URLField

class Playlist(Model):
    name = CharField("Playlist Name")
    apple_url = URLField("Apple Music URL", null = True, unique = True)
    gpm_url = URLField("Google Play Music URL", null = True, unique = True)
    soundcloud_url = URLField("Soundcloud URL", null = True, unique = True)
    spotify_url = URLField("Spotify URL", null = True, unique = True)
    artwork = URLField("Playlist image URL")
