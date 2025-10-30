from rest_framework import viewsets, mixins
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .serializers import (
    PostSerializer,
    CommentSerializer,
    FollowSerializer,
    GroupSerializer
)
from .permissions import IsAuthorOrReadOnly
from posts.models import Post, Group

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
