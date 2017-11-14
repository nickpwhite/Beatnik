from django.db import models

class Song(models.Model):
    gpm_id = models.CharField("Google Play Music ID", max_length=200)
    spotify_id = models.CharField("Spotify ID", max_length=200)
    apple_id = models.CharField("Apple Music ID", max_length=200)
    soundcloud_id = models.CharField("Soundcloud ID", max_length=200)
    match_rating = models.IntegerField("Rating of the match", default=0)

class Album(models.Model):
    gpm_id = models.CharField("Google Play Music ID", max_length=200)
    spotify_id = models.CharField("Spotify ID", max_length=200)
    apple_id = models.CharField("Apple Music ID", max_length=200)
    soundcloud_id = models.CharField("Soundcloud ID", max_length=200)
    match_rating = models.IntegerField("Rating of the match", default=0)
