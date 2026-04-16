from rest_framework import serializers
from .models import UserProfile, Post, Media, Follow, Like, Comment, Note, Story


# Тіркелу сериализаторы
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)


# Пайдаланушы профилі
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'bio', 'avatar_url', 'created_at']


# Медиа
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'url', 'mime_type', 'width', 'height', 'order_idx']


# Посттар (медиамен бірге)
class PostSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.CharField(source='author.avatar_url', read_only=True)
    likes_count = serializers.IntegerField(source='post_likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_username', 'author_avatar',
            'caption', 'media', 'likes_count', 'comments_count', 'created_at'
        ]
        read_only_fields = ['author', 'created_at']


# Жазылу
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


# Лайк
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


# Пікір
class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'text', 'created_at']
        read_only_fields = ['author', 'created_at']


# Заметка
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


# Сторис
class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'