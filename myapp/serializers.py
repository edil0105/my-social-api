from rest_framework import serializers
from .models import UserProfile, Post, Media, Follow, Like, Comment, Note, Story


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    email    = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)


class SearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserProfile
        fields = ['id', 'username', 'avatar_url', 'bio']


class UserProfileSerializer(serializers.ModelSerializer):
    posts_count     = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model  = UserProfile
        fields = ['id', 'username', 'email', 'bio', 'avatar_url', 'created_at',
                  'posts_count', 'followers_count', 'following_count']

    def get_posts_count(self, obj):
        return obj.posts.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Media
        fields = ['id', 'url', 'mime_type', 'width', 'height', 'order_idx']


class PostSerializer(serializers.ModelSerializer):
    media          = MediaSerializer(many=True, read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_avatar   = serializers.CharField(source='author.avatar_url', read_only=True)
    likes_count    = serializers.IntegerField(source='post_likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model  = Post
        fields = ['id', 'author', 'author_username', 'author_avatar',
                  'caption', 'media', 'likes_count', 'comments_count', 'created_at']
        read_only_fields = ['author', 'created_at']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Follow
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model  = Comment
        fields = ['id', 'post', 'author', 'author_username', 'text', 'created_at']
        read_only_fields = ['author', 'created_at']


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Note
        fields = '__all__'


class StorySerializer(serializers.ModelSerializer):
    username   = serializers.CharField(source='user.username', read_only=True)
    avatar_url = serializers.CharField(source='user.avatar_url', read_only=True)

    class Meta:
        model  = Story
        fields = ['id', 'user', 'username', 'avatar_url', 'image', 'created_at', 'expires_at']
        read_only_fields = ['user', 'created_at', 'expires_at']