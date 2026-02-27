from rest_framework import serializers
from .models import UserProfile, Post, Media, Follow, Like, Comment, RefreshToken

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

from rest_framework import serializers
from .models import Post, Media

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'url', 'mime_type', 'order_idx']

class PostSerializer(serializers.ModelSerializer):
    # 'media_set' немесе модельдегі related_name атауы
    # Бұл жол постқа байланған барлық медианы шығарады
    media = MediaSerializer(many=True, read_only=True, source='media_set')

    class Meta:
        model = Post
        fields = ['id', 'author', 'caption', 'media'] # 'media' өрісін қостық
        
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class RefreshTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefreshToken
        fields = '__all__'