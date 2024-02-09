from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)

from api.viewsets import ListCreateModelViewSet
from api.permissions import IsAuthorOrAuthenticatedReadOnly
from api.serializers import (CommentModelSerializer, FollowModelSerializer,
                             GroupModelSerializer, PostModelSerializer)
from posts.models import Group, Post


class FollowModelViewSet(ListCreateModelViewSet):
    serializer_class = FollowModelSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.followers.select_related('following')

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.select_related('author')
    serializer_class = PostModelSerializer
    permission_classes = (IsAuthorOrAuthenticatedReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )


class GroupReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    permission_classes = (AllowAny,)


class CommentModelViewSet(ModelViewSet):
    serializer_class = CommentModelSerializer
    permission_classes = (IsAuthorOrAuthenticatedReadOnly,)

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        post = self.get_post()
        return post.comments.select_related('author')

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(
            post=post,
            author=self.request.user
        )
