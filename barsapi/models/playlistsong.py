from django.db import models
from django.db.models.deletion import CASCADE
from .playlist import Playlist
from .song import Song

class PlaylistSong(models.Model):
    playlist = models.OneToOneField(Playlist, on_delete=CASCADE)
    song = models.OneToOneField(Song, on_delete=CASCADE)