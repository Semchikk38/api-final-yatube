from rest_framework import serializers
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Follow, Group

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ('author',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

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
        user = self.context['request'].user

        if user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )

        if Follow.objects.filter(user=user, following=value).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя'
            )

        return value


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group
