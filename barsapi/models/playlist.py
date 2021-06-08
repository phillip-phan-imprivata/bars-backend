from django.db import models
from .barsuser import BarsUser

class Playlist(models.Model):
    name = models.CharField(max_length=50)
    barsuser = models.OneToOneField(BarsUser, on_delete=models.CASCADE)