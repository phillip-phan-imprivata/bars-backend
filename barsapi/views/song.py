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
        fields = ('id', 'song_link', 'title', 'channel', 'thumbnail')

class Songs(ViewSet):
    def list(self, request):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = api_key
        search_query = self.request.query_params.get('search', None)

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = DEVELOPER_KEY)

        api_request = youtube.search().list(
            part="snippet",
            q=search_query,
            maxResults=10,
        )
        response = api_request.execute()

        search_results = []
        for item in response["items"]:
            if item["id"]["kind"] == "youtube#video":
                search_results.append(item)

        return Response(search_results)
