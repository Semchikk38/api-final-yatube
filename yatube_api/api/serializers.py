from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Follow, Group

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = SlugRelatedField(
        slug_field='id',
        queryset=Group.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ('author',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'post')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return value


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group
