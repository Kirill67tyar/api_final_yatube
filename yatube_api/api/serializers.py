from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import (CurrentUserDefault, ModelSerializer,
                                        SlugRelatedField, ValidationError)
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post


User = get_user_model()


class FollowModelSerializer(ModelSerializer):
    user = SlugRelatedField(
        default=CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )
    following = SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = (
            'user', 'following',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following',),
                message=(
                    'Ошибка: вы уже подписаны на пользователя'
                    'доступного по ключу "following".'
                    'Нельзя подписываться дважды.'
                )
            ),
        ]

    def validate_following(self, value):
        user = self.context['request'].user
        following = get_object_or_404(User, username=value)
        if user == following:
            raise ValidationError(
                'Ошибка: нельзя подписываться на самого себя.'
            )
        return value


class PostModelSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'author',
            'image',
            'group',
            'pub_date',
        )


class GroupModelSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'slug',
            'description',
        )


class CommentModelSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'post',
            'text',
            'created',
        )
        read_only_fields = ('post',)
