from django.db import models

class Song(models.Model):
    name = models.CharField("Track Name", max_length=200)
    artist = models.CharField("Artist Name", max_length=200)
    gpm_id = models.CharField("Google Play Music ID", max_length=200)
    spotify_id = models.CharField("Spotify ID", max_length=200)
    apple_id = models.CharField("Apple Music ID", max_length=200)
    soundcloud_id = models.CharField("Soundcloud ID", max_length=200)
    match_rating = models.IntegerField("Rating of the match", default=0)
    insertion_date = models.DateTimeField("Date of initial insertion")
    update_date = models.DateTimeField("Date of last update")
    artwork = models.URLField()

class Album(models.Model):
    name = models.CharField("Album Name", max_length=200)
    artist = models.CharField("Artist Name", max_length=200)
    gpm_id = models.CharField("Google Play Music ID", max_length=200)
    spotify_id = models.CharField("Spotify ID", max_length=200)
    apple_id = models.CharField("Apple Music ID", max_length=200)
    soundcloud_id = models.CharField("Soundcloud ID", max_length=200)
    match_rating = models.IntegerField("Rating of the match", default=0)
    insertion_date = models.DateTimeField("Date of initial insertion")
    update_date = models.DateTimeField("Date of last update")
    artwork = models.URLField()
