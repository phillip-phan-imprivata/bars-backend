from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from barsapi.models import Playlist, Song
import os
import googleapiclient.discovery

api_key = "AIzaSyDiw-lKDm059fMzzY0lMYGvaEKwX1zJMb0"

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'song_link', 'title', 'channel',)

class Songs(ViewSet):
    def list(self, request):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = api_key
        search_query = request.data["search"]

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = DEVELOPER_KEY)

        api_request = youtube.search().list(
            part="snippet",
            q=search_query
        )
        response = api_request.execute()

        return Response(response)

    def create(self, request):
        new_song = Song()
        new_song.song_link = request.data["songLink"]
        new_song.title = request.data["title"]
        new_song.channel = request.data["channel"]
        new_song.save()

        serializer = SongSerializer(
            new_song, context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)