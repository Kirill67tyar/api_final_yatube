# from rest_framework.serializers import (
#     ModelSerializer,
#     SlugRelatedField,
# )

# from posts.models import Comment, Group, Post
# from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField


# from posts.models import Comment, Post


# class PostSerializer(serializers.ModelSerializer):
#     author = SlugRelatedField(slug_field='username', read_only=True)

#     class Meta:
#         fields = '__all__'
#         model = Post


# class CommentSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(
#         read_only=True, slug_field='username'
#     )

#     class Meta:
#         fields = '__all__'
#         model = Comment


# !-----------------------------
from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField,
)

from posts.models import Comment, Group, Post


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