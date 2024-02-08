from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)

from api.permissions import IsAuthorOrAuthenticatedReadOnly
from api.serializers import (CommentModelSerializer, FollowModelSerializer,
                             GroupModelSerializer, PostModelSerializer)
from posts.models import Group, Post


class FollowModelViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    serializer_class = FollowModelSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.select_followers.select_related('following')


class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.select_related('author')
    serializer_class = PostModelSerializer
    permission_classes = (IsAuthorOrAuthenticatedReadOnly,)
    pagination_class = LimitOffsetPagination


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
