from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, base_name='users')
router.register('groups', views.GroupViewSet)
router.register('online_user_live_listenings',views.online_user_live_listenings, base_name='online_user_live_listenings')
router.register('tracks',views.tracks, base_name='tracks')
router.register('user_history/(?P<user_id>.+)',views.user_track_history, base_name='user_track_history')
#router.register('admin_user_track_history/(?P<user_id>.+)/', views.admin_user_track_history, base_name='admin_user_track_history'),
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]