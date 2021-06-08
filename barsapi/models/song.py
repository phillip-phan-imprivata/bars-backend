from django.db import models
from .playlist import Playlist

class Song(models.Model):
    song_link = models.CharField(max_length=100)