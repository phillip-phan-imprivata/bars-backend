from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from barsapi.models import Playlist
import os
import googleapiclient.discovery

api_key = "AIzaSyDiw-lKDm059fMzzY0lMYGvaEKwX1zJMb0"

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