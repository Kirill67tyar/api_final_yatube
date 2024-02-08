from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.permissions import IsAuthorOrAuthenticatedReadOnly
from api.serializers import (CommentModelSerializer, GroupModelSerializer,
                             PostModelSerializer)
from posts.models import Group, Post


class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.select_related('author')
    serializer_class = PostModelSerializer
    permission_classes = (IsAuthorOrAuthenticatedReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(
            post=post,
            author=self.request.user
        )
