
from django.urls import path, include
from . import views

app_name='spotify_app'


urlpatterns = [
    path('weekly_chart/', views.weekly_chart,name='weekly_chart'),
    path('recommended_songs/', views.recommended_songs,name='recommended_songs'),
    path('stream/<int:user_id>', views.stream,name='stream'),
    path('lyrics/<str:track_id>/<str:artist_id>', views.lyrics_track,name='lyrics'),
    path('user_history/', views.user_history,name='user_history'),
]
