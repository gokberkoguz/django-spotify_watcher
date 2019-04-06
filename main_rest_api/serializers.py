from django.contrib.auth.models import User, Group
from spotify_app.models import track_object,user_track_history
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class track_serializer(serializers.ModelSerializer):
    class Meta:
        model = track_object
        fields = ('name','uri','artist')

class online_user_live_listenings_serializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)
    timestamp = serializers.DateTimeField()

    def create(self, validated_data):
        return tracks(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance

class tracks(object):
    def __init__(self, **kwargs):
        for field in ('id', 'name', 'timestamp'):
            setattr(self, field, kwargs.get(field, None))

class user_history(serializers.ModelSerializer):
    id = serializers.CharField(source="track.id")
    artist = serializers.ListField(source="track.artist")
    name = serializers.CharField(source="track.name")
    user_id = serializers.CharField(source="user.id")
    # username = serializers.CharField(source="user.display_name")
    class Meta:
        model = user_track_history
        fields = ('played_at','id','name','user_id','artist')
