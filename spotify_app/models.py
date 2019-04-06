from django.db import models
from django.contrib.postgres.fields import JSONField , ArrayField
from django.core import serializers
from django.db import transaction
from django.http import JsonResponse
from django.forms.models import model_to_dict


"""
MAYBE RAW SQL MIGHT BE BETTER TO IMPLEMENT 
"""


class followers_object(models.Model):
    id = models.AutoField(primary_key=True)
    href = models.CharField(max_length=255 ,null=True)
    total = models.IntegerField(null=True)

class external_ids(models.Model):
    id = models.AutoField(primary_key=True)
    json = JSONField()

class external_urls(models.Model):
    id= models.AutoField(primary_key=True)
    json = JSONField()

class image_object(models.Model):
    images = JSONField(default=list,primary_key=True)

class restriction(models.Model):
    restriction= JSONField(primary_key=True)

class copyrights(models.Model):
    text = models.CharField(max_length=255 ,null=True)
    type = models.CharField(max_length=255 ,null=True)

class audio_features_object(models.Model):
    acousticness = models.FloatField()
    analysis_url = models.CharField(max_length=255 ,null=True)
    danceability = models.FloatField()
    duration_ms = models.IntegerField()
    energy = models.FloatField()
    id = models.CharField(max_length=255 , primary_key=True)
    instrumentalness = models.FloatField()
    key = models.IntegerField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    mode = models.IntegerField()
    speechiness = models.FloatField()
    tempo = models.FloatField()
    time_signature = models.IntegerField()
    track_href = models.CharField(max_length=255 ,null=True)
    type = models.CharField(max_length=255 ,null=True)
    uri = models.CharField(max_length=255 ,null=True)
    valence = models.FloatField()

class catagory_object(models.Model):
    href = models.CharField(max_length=255 ,null=True)
    icons = models.ForeignKey(image_object , on_delete=models.CASCADE ,null=True)
    id = models.CharField(max_length=255 ,primary_key=True)
    name = models.CharField(max_length=255 ,null=True)

class context_object(models.Model):
    type = models.CharField(max_length=255 ,null=True)
    href = models.CharField(max_length=255 ,null=True)
    external_urls = models.ForeignKey(external_urls, on_delete=models.CASCADE)
    uri = models.CharField(max_length=255, null=True)

    @transaction.atomic
    def save(self, *args, **kwargs):

        if external_urls.objects.filter(json=self.external_urls.json).exists():
            self.external_urls = external_urls.objects.filter(json=self.external_urls.json)[0]
            print(self.external_urls)
        else:
            self.external_urls.save()
            self.external_urls = external_urls.objects.filter(json=self.external_urls.json)[0]

        super(context_object, self).save(*args, **kwargs)

class cursor_object(models.Model):
    after = models.CharField(max_length=255, null=True)

class play_history_object(models.Model):
    track = models.ForeignKey(image_object,on_delete=models.CASCADE ,null=True)
    played_at = models.DateTimeField()
    context = models.OneToOneField(context_object , on_delete=models.CASCADE,null=True)

class error_object(models.Model):
    status = models.IntegerField()
    message= models.CharField(max_length=255 ,null=True)

class play_error_object(models.Model):
    status = models.IntegerField()
    message = models.CharField(max_length=255, null=True)
    reason = models.CharField(max_length=255, null=True)

class user_object(models.Model):
    '''
    Private user object will be added
    '''
    display_name = models.CharField(max_length=255, null=True)
    external_urls = models.ForeignKey(external_urls, on_delete=models.CASCADE)
    followers = models.OneToOneField(followers_object, on_delete=models.CASCADE, null=True)
    href = models.CharField(max_length=255, null=True)
    id = models.CharField(max_length=255, primary_key=True)
    images = models.ForeignKey(image_object, on_delete=models.CASCADE, null=True)
    type=models.CharField(max_length=255)
    uri = models.CharField(max_length=255)

    @transaction.atomic
    def save(self, *args, **kwargs):

        if followers_object.objects.filter(id=self.followers.id).exists():
            self.followers = followers_object.objects.get(id=self.followers.id)
        else:
            self.followers.save()

        if external_urls.objects.filter(json=self.external_urls.json).exists():
            self.external_urls = external_urls.objects.filter(json=self.external_urls.json)[0]
        else:
            self.external_urls.save()
            self.external_urls = external_urls.objects.filter(json=self.external_urls.json)[0]

        if image_object.objects.filter(images=self.images.images).exists():
            self.images = image_object.objects.get(images=self.images.images)
        else:
            self.images.save()
        super(user_object, self).save(*args, **kwargs)

class user_object_private(models.Model):
    pass

class recommendations_seed_object(models.Model):
    afterFilteringSize=models.IntegerField()
    afterRelinkingSize = models.IntegerField()
    href = models.CharField(max_length=255, null=True)
    id = models.CharField(max_length=255, primary_key=True)
    initialPoolSize = models.IntegerField()
    type = models.CharField(max_length=255)



class recommendations_object():
    seeds= ArrayField(JSONField(),primary_key=True)
    tracks = ArrayField(JSONField())

class playlist_object(models.Model):
    collaborative=models.BooleanField()
    description = models.CharField(max_length=255, null=True)
    external_urls = models.ForeignKey(external_urls,on_delete=models.CASCADE)
    followers = models.OneToOneField(followers_object, on_delete=models.CASCADE, null=True)
    href = models.CharField(max_length=255, null=True)
    id = models.CharField(max_length=255, primary_key=True)
    images = models.ForeignKey(image_object, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)
    owner = models.ForeignKey(user_object, on_delete=models.CASCADE, null=True)
    public = models.BooleanField()
    snapshot_id = models.CharField(max_length=255, null=True)
    tracks = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    uri = models.CharField(max_length=255, null=True)

    @transaction.atomic
    def save(self, *args, **kwargs):

        if external_urls.objects.filter(json=self.external_urls.json).exists():
            self.external_urls = external_urls.objects.filter(json=self.external_urls.json)[0]
        else:
            self.external_urls.save()
            self.external_urls = external_urls.objects.filter(json=self.external_urls.json)[0]

        if image_object.objects.filter(images=self.images.images).exists():
            self.images = image_object.objects.get(images=self.images.images)
        else:
            self.images.save()

        if user_object.objects.filter(id=self.owner.id).exists():
            self.owner = user_object.objects.get(id=self.owner.id)
        else:

            self.owner.save()
            self.owner = user_object.objects.get(id=self.owner.id)

        super(playlist_object, self).save(*args, **kwargs)
class artist_object_new(models.Model):


    external_urls = models.ForeignKey(external_urls,on_delete=models.CASCADE)
    followers= models.OneToOneField(followers_object , on_delete=models.CASCADE,null=True)
    genres = ArrayField(models.CharField(max_length=255), null=True, blank=True)
    href = models.CharField(max_length=255 ,null=True )
    images = models.ForeignKey(image_object,on_delete=models.CASCADE ,null=True)
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255 ,null=True)
    popularity = models.IntegerField(null=True)
    type = models.CharField(max_length=255 ,null=True)
    uri = models.CharField(max_length=255 ,null=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if external_urls.objects.filter(json=self.external_urls.json).exists():
            self.external_urls = external_urls.objects.filter(json=self.external_urls.json)[0]
        else:
            self.external_urls.save()
            self.external_urls = external_urls.objects.filter(json=self.external_urls.json)[0]


        super(artist_object_new, self).save(*args, **kwargs)


class album_object(models.Model):
    album_group = models.CharField(max_length=255 ,null=True )
    album_type = models.CharField(max_length=255 ,null=True )
    artist = JSONField(null=True)
    available_markets = ArrayField(models.CharField(max_length=255), null=True, blank=True)
    copyrights = models.OneToOneField(copyrights , on_delete=models.CASCADE,null=True)
    external_urls = models.ForeignKey(external_urls,on_delete=models.CASCADE,null=True)
    genres = ArrayField(models.CharField(max_length=255), null=True, blank=True)
    href = models.CharField(max_length=255 ,null=True )
    id = models.CharField(max_length=255, primary_key=True)
    images = models.ForeignKey(image_object,on_delete=models.CASCADE ,null=True)
    label = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    popularity = models.IntegerField(null=True)
    release_date = models.CharField(max_length=255 ,null=True)
    release_date_precision = models.CharField(max_length=255 ,null=True)
    restrictions = models.OneToOneField(restriction,on_delete=models.CASCADE ,null=True)
    type = models.CharField(max_length=255 ,null=True)
    uri = models.CharField(max_length=255 ,null=True)
    tracks = ArrayField(JSONField(), null=True, blank=True)
    @transaction.atomic
    def save(self, *args, **kwargs):
        if external_urls.objects.filter(json=self.external_urls.json).exists():
            self.external_urls = external_urls.objects.filter(json=self.external_urls.json)[0]
        else:
            self.external_urls.save()
            self.external_urls = external_urls.objects.filter(json=self.external_urls.json)[0]
        if image_object.objects.filter(images=self.images.images).exists():
            self.images = image_object.objects.get(images=self.images.images)
        else:
            self.images.save()

        super(album_object, self).save(*args, **kwargs)
class linked_track_object(models.Model):
    external_urls = models.ForeignKey(external_urls, on_delete=models.CASCADE)
    href = models.CharField(max_length=255, null=True)
    id = models.CharField(max_length=255, primary_key=True)
    type = models.CharField(max_length=255 ,null=True)
    uri = models.CharField(max_length=255 ,null=True)



class track_object(models.Model):

    album = models.ForeignKey(album_object, on_delete=models.CASCADE, null=True)
    artist = JSONField(null=True)
    #available_markets = models.CharField(max_length=255 ,null=True)
    disc_number = models.IntegerField(null=True)
    duration_ms = models.IntegerField(null=True)
    explicit = models.BooleanField(null=True)
    external_ids= models.ForeignKey(external_ids,on_delete=models.CASCADE,null=True)
    external_urls = models.ForeignKey(external_urls,on_delete=models.CASCADE,null=True)
    href = models.CharField(max_length=255, null=True)
    id = models.CharField(max_length=255, primary_key=True)
    is_playable = models.BooleanField(null=True)
    linked_from = models.ForeignKey(linked_track_object,on_delete=models.CASCADE,null=True)
    restrictions = models.ForeignKey(restriction,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255,null=True)
    popularity = models.IntegerField(null=True)
    preview_url = models.CharField(max_length=255,null=True)
    track_number = models.IntegerField(null=True)
    type = models.CharField(max_length=255, null=True)
    uri = models.CharField(max_length=255, null=True)
    is_local=models.BooleanField(null=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if external_urls.objects.filter(json=self.external_urls.json).exists():
            self.external_urls = external_urls.objects.filter(json=self.external_urls.json)[0]
        else:
            self.external_urls.save()
            self.external_urls = external_urls.objects.filter(json=self.external_urls.json)[0]
        if external_ids.objects.filter(json=self.external_ids.json).exists():
            self.external_ids = external_ids.objects.get(json=self.external_ids.json)
        else:
            self.external_ids.save()
        if album_object.objects.filter(id=self.album.id).exists():
            self.album = album_object.objects.get(id=self.album.id)
        else:
            self.album.save()
            self.album = album_object.objects.get(id=self.album.id)

        super(track_object, self).save(*args, **kwargs)

class user_track_history(models.Model):
    played_at = models.DateTimeField(primary_key=True)
    user = models.ForeignKey(user_object,on_delete=models.DO_NOTHING)
    track = models.ForeignKey(track_object, on_delete=models.DO_NOTHING)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if track_object.objects.filter(id=self.track.id).exists():
            self.track = track_object.objects.get(id=self.track.id)
        else:
            self.track.save()
            self.track = track_object.objects.get(id=self.track.id)

        super(user_track_history, self).save(*args, **kwargs)

class currently_playing_object(models.Model):
    timestamp = models.DateTimeField(null=True)
    user = models.ForeignKey(user_object, on_delete=models.CASCADE, null=True)
    context = models.ForeignKey (context_object, on_delete=models.CASCADE, null=True)
    progress_ms = models.IntegerField(null=True)
    is_playing = models.BooleanField(null=True)
    track = models.CharField(max_length=255, null=True)
    currently_playing_type = models.CharField(max_length=255, null=True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.context:
            if context_object.objects.filter(uri=self.context.uri).exists():
                self.context = context_object.objects.filter(uri=self.context.uri)[0]
            else:
                self.context.save()
                self.context = context_object.objects.filter(uri=self.context.uri)[0]
        if currently_playing_object.objects.filter(user=self.user,is_playing=self.is_playing,track=self.track,timestamp=self.timestamp).exists():
            currently_playing_object.objects.filter(user=self.user,is_playing=self.is_playing,track=self.track).update(progress_ms=self.progress_ms)
        else:
            currently_playing_object.objects.filter(user=self.user).exclude(track=self.track,timestamp=self.timestamp).update(is_playing=False)
            super(currently_playing_object, self).save(*args, **kwargs)

class playlist_track_object(models.Model):
    added_at = models.DateTimeField()
    added_by = models.ForeignKey(user_object, on_delete=models.CASCADE, null=True)
    is_local = models.BooleanField()
    track = models.ForeignKey(track_object, on_delete=models.CASCADE, null=True)

class saved_track_object():
    added_at = models.DateTimeField()
    track = models.ForeignKey(track_object, on_delete=models.CASCADE, null=True)

class saved_album_object():
    added_at = models.DateTimeField()
    track = models.ForeignKey(album_object, on_delete=models.CASCADE, null=True)

class streaming_users():
    user = models.ForeignKey(user_object, on_delete=models.DO_NOTHING)
    stream = models.BooleanField
