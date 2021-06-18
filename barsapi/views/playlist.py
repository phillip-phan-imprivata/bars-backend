from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from barsapi.models import Playlist, BarsUser, PlaylistSong, Song

class PlaylistSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistSong
        fields = ('id', 'song',)
        depth = 1

class PlaylistWithSongsSerializer(serializers.ModelSerializer):
    songs = PlaylistSongSerializer(many=True)

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'barsuser', 'songs',)

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

    def retrieve(self, request, pk=None):
        try:
            barsuser = BarsUser.objects.get(user=request.auth.user)
            playlist = Playlist.objects.get(pk=pk, barsuser=barsuser)
            playlist.songs = PlaylistSong.objects.filter(playlist=playlist)

            serializer = PlaylistWithSongsSerializer(
                playlist, many=False, context={'request': request}
            )
            return Response(serializer.data)

        except Playlist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        barsuser = BarsUser.objects.get(user=request.auth.user)
        new_playlist = Playlist()
        new_playlist.name = request.data["name"]
        new_playlist.barsuser = barsuser
        new_playlist.save()

        serializer = PlaylistSerializer(
            new_playlist, many=False, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post', 'delete'], detail=False)
    def playlistsong(self, request):
        if request.method == "POST":
            barsuser = BarsUser.objects.get(user=request.auth.user)
            try:
                playlist = Playlist.objects.get(pk=request.data["playlistId"], barsuser=barsuser)

                try:
                    song = Song.objects.get(song_link=request.data["songLink"])
                    playlistsong = PlaylistSong.objects.get(playlist=playlist, song=song)
                    
                    return Response(
                        {'message': 'Song already added to this playlist.'},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY
                    )

                except Song.DoesNotExist as ex:
                    song = Song()
                    song.song_link = request.data["songLink"]
                    song.title = request.data["title"]
                    song.channel = request.data["channel"]
                    song.thumbnail = request.data["thumbnail"]
                    song.save()

                    playlistsong = PlaylistSong()
                    playlistsong.playlist = playlist
                    playlistsong.song = song
                    playlistsong.save()

                    return Response(None, status=status.HTTP_201_CREATED)

                except PlaylistSong.DoesNotExist as ex:
                    playlistsong = PlaylistSong()
                    playlistsong.playlist = playlist
                    playlistsong.song = song
                    playlistsong.save()

                    return Response(None, status=status.HTTP_201_CREATED)
            
            except Playlist.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        if request.method == "DELETE":
            try:
                barsuser = BarsUser.objects.get(user=request.auth.user)
                playlist = Playlist.objects.get(pk=request.data["playlistId"], barsuser=barsuser)
                song = Song.objects.get(pk=request.data['songId'])

                playlistsong = PlaylistSong.objects.get(playlist=playlist, song=song)
                playlistsong.delete()

                try:
                    playlistsongs = PlaylistSong.objects.filter(song=song)
                    if len(playlistsongs) == 0:
                        song.delete()                   
                    return Response({}, status=status.HTTP_204_NO_CONTENT)
                
                except Exception as ex:
                    return Response({}, status=status.HTTP_204_NO_CONTENT)
            
            except Playlist.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            except Song.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(None, status=status.HTTP_405_METHOD_NOT_ALLOWED)