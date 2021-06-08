from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from barsapi.models import Playlist, BarsUser

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('id', 'name', 'barsuser',)

class Playlists(ViewSet):
    def list(self, request):
        barsuser = BarsUser.objects.get(user = request.auth.user)
        playlists = Playlist.objects.filter(barsuser = barsuser)

        serializer = PlaylistSerializer(
            playlists, many=True, context={'request': request}
        )

        return Response(serializer.data)

    def update(self, request, pk=None):
        barsuser = BarsUser.objects.get(user=request.auth.user)
        playlist = Playlist.objects.get(pk=pk, barsuser=barsuser)

        playlist.name = request.data["name"]
        playlist.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            barsuser = BarsUser.objects.get(user=request.auth.user)
            playlist = Playlist.objects.get(pk=pk, barsuser=barsuser)
            playlist.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Playlist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

