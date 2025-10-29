from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('follow', FollowViewSet, basename='follow')
router.register('groups', GroupViewSet, basename='groups')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
