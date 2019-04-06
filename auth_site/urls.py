
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
app_name='auth_home'

urlpatterns = [
    #path('', include('social_django.urls', namespace='social')),
    path('', include('auth_home.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('spotify/', include('spotify_app.urls')),
    #path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL},name='logout'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('main_rest_api.urls'))
]
