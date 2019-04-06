from django.shortcuts import render
from django.contrib.auth.models import User
from spotify_app import spotify_api
import requests

def weekly_chart(request):
    if request.user.is_authenticated:
        print('USER ACCESS')
        print(request.user)
    else:
        print(request.user)
    return render(request, 'weekly_chart.html')


def recommended_songs(request):


    users = User.objects.all()
    for user_object in users:
        if user_object.username!='mgokberk':

                social = user_object.social_auth.get(provider='spotify')
                refresh = spotify_api.SpotifyRefreshUsers()

                refresh.refresh_token()
                spotify_wrapper = spotify_api.SpotifyApi(social)
                lines = spotify_wrapper.user_track_history()
                print(lines,'test')
                #spotify_wrapper.next_track()


    #user = User.objects.get(username='enivecivokke')
    #social = user.social_auth.get(provider='spotify')
    #token = social.extra_data['access_token']
    #ref_token = social.extra_data['access_token']
    #spotify_wrapper = SpotifyApi(token,ref_token)
    #spotify_wrapper.get_playlists()
    #print(request.user)
    #user = User.objects.get(username=request.user)
    #print(user)
    #social = user.social_auth.get(provider='spotify')
    #token = social.extra_data['access_token']
    #print(token)
    #spotify=spotify_api(token,refresh_token)
    '''
    user = User.objects.get(id=1)
    social = user.social_auth.get(provider='spotify')
    token=social.extra_data['access_token']
    '''

    return render(request, 'recommended_songs.html', {'lyrics':lines})

def stream(request,user_id):
    user = User.objects.get(id= user_id)
    social_user = user.social_auth.get(provider='spotify')
    token = social_user.extra_data['access_token']
    spotify_wrapper = spotify_api.SpotifyApi(social_user)
    spotify_wrapper.get_user_currently_playing()
    return render(request, 'spotify_player.html',{'access_token':token})

def lyrics_track(request,track_id,artist_id):

    user = User.objects.get(id=request.user.id)
    social_user = user.social_auth.get(provider='spotify')
    token = social_user.extra_data['access_token']
    spotify_wrapper = spotify_api.SpotifyApi(social_user)
    lyrics = spotify_wrapper.prepare_track(track_id,artist_id)
    return render(request, 'lyrics.html', {'lyrics': lyrics})

def user_history(request):
    r = requests.get("http://127.0.0.1:8000/api/v1/user_history/" + str(request.user.id))

    return render(request, 'history.html', {'tracks': r.json()['results']})