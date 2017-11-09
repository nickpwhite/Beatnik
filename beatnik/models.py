from django.db import models

class Song(models.Model):
    gpm_id = models.CharField(max_length=200)
    spotify_id = models.CharField(max_length=200)
    apple_id = models.CharField(max_length=200)
    soundcloud_id = models.CharField(max_length=200)

class Album(models.Model):
    gpm_id = models.CharField(max_length=200)
    spotify_id = models.CharField(max_length=200)
    apple_id = models.CharField(max_length=200)
    soundcloud_id = models.CharField(max_length=200)
