from django.db import models
from .playlist import Playlist

class Song(models.Model):
    song_link = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    channel = models.CharField(max_length=50)