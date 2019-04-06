from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer,online_user_live_listenings_serializer,track_serializer,user_history
from spotify_app.models import currently_playing_object,track_object , user_track_history as spotify_user_track_history
from datetime import timedelta, datetime as dt
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

#
# class admin_user_track_history(viewsets.ModelViewSet):
#     #permission_classes = (permissions.IsAdminUser,)
#     #authentication_classes = (SessionAuthentication, BasicAuthentication)
#     serializer_class = user_track_history_serializer
#
#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
#         return user_tracks_history.objects.filter(user_id= user_id,
#                                                   timestamp__range=(dt.now() - timedelta(days=30), dt.now()))

class user_track_history(viewsets.ModelViewSet):
    #permission_classes = (permissions.IsAdminUser,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = user_history

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return spotify_user_track_history.objects.filter(user_id=User.objects.get(id= user_id).username).order_by('played_at')


class tracks(viewsets.ModelViewSet):

    serializer_class = track_serializer

    def get_queryset(self):
        return track_object.objects.all()



class online_user_live_listenings(viewsets.ViewSet):
    #permission_classes = (permissions.IsAdminUser,)
    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = online_user_live_listenings_serializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = online_user_live_listenings_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
         return currently_playing_object.objects.raw("""SELECT sp.id,sp.timestamp,e.name,e.uri FROM spotify_app_currently_playing_object AS sp
                 LEFT JOIN spotify_app_track_object as e on sp.track = e.id
                 WHERE is_playing=TRUE""")

