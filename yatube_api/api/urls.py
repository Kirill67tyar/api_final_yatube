from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CommentModelViewSet, FollowModelViewSet,
                       GroupReadOnlyModelViewSet, PostModelViewSet)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(
    'posts',
    PostModelViewSet,
    basename='posts'
)
router_v1.register(
    'groups',
    GroupReadOnlyModelViewSet,
    basename='groups',
)
router_v1.register(
    'follow',
    FollowModelViewSet,
    basename='follow',
)
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentModelViewSet,
    basename='comments'
)

urlpatterns_v1 = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]

urlpatterns = [
    path(
        'v1/',
        include(urlpatterns_v1),
    ),
]
