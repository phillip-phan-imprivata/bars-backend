from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from barsapi.models import Playlist, BarsUser, PlaylistSong, Song

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('id', 'name', 'barsuser',)

class PlaylistSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistSong
        fields = ('id', 'song',)
        depth = 1

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

    def retrieve(self, request, pk=None):
        playlist = Playlist.objects.get(pk=pk)
        playlist_songs = PlaylistSong.objects.filter(playlist=playlist)

        serializer = PlaylistSongSerializer(
            playlist_songs, many=True, context={'request': request}
        )

        return Response(serializer.data)



    @action(methods=['post', 'delete'], detail=True)
    def playlistsong(self, request, pk=None):
        if request.method == "POST":
            playlist = Playlist.objects.get(pk=pk)
            song = Song.objects.get(pk=request.data["songId"])

            try:
                playlistsong = PlaylistSong.objects.get(playlist=playlist, song=song)
                return Response(
                    {'message': 'Song already added to this playlist.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )

            except PlaylistSong.DoesNotExist as ex:
                playlistsong = PlaylistSong()
                playlistsong.playlist = playlist
                playlistsong.song = song
                playlistsong.save()

                return Response(None, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            try:
                playlist = Playlist.objects.get(pk=pk)
                song = Song.objects.get(pk=request.data['songId'])

                playlistsong = PlaylistSong.objects.get(playlist=playlist, song=song)
                playlistsong.delete()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            
            except Playlist.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            except Song.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)