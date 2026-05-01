from rest_framework import serializers
from .models import (
    UserProfile, Post, Media, Follow, Like,
    Comment, Note, Story, DirectMessage, Conversation
)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    email    = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    posts_count     = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model  = UserProfile
        fields = ['id', 'username', 'email', 'bio', 'avatar_url',
                  'created_at', 'posts_count', 'followers_count', 'following_count']

    def get_posts_count(self, obj):     return obj.posts.count()
    def get_followers_count(self, obj): return obj.followers.count()
    def get_following_count(self, obj): return obj.following.count()


class SearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserProfile
        fields = ['id', 'username', 'avatar_url', 'bio']


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Media
        fields = ['id', 'url', 'mime_type', 'width', 'height', 'order_idx']


class PostSerializer(serializers.ModelSerializer):
    media           = MediaSerializer(many=True, read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_avatar   = serializers.CharField(source='author.avatar_url', read_only=True)
    likes_count     = serializers.IntegerField(source='post_likes.count', read_only=True)
    comments_count  = serializers.IntegerField(source='comments.count', read_only=True)
    is_liked        = serializers.SerializerMethodField()

    class Meta:
        model  = Post
        fields = ['id', 'author', 'author_username', 'author_avatar',
                  'caption', 'media', 'likes_count', 'comments_count',
                  'is_liked', 'created_at']
        read_only_fields = ['author', 'created_at']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                profile = request.user.profile
                return obj.post_likes.filter(user=profile).exists()
            except Exception:
                pass
        return False


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
    author_avatar   = serializers.CharField(source='author.avatar_url', read_only=True)

    class Meta:
        model  = Comment
        fields = ['id', 'post', 'author', 'author_username', 'author_avatar', 'text', 'created_at']
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


# ── Direct Message ──────────────────────────────────────────────────────────

class DirectMessageSerializer(serializers.ModelSerializer):
    sender_username   = serializers.CharField(source='sender.username', read_only=True)
    sender_avatar     = serializers.CharField(source='sender.avatar_url', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model  = DirectMessage
        fields = ['id', 'sender', 'sender_username', 'sender_avatar',
                  'receiver', 'receiver_username', 'text', 'is_read', 'created_at']
        read_only_fields = ['sender', 'is_read', 'created_at']


class SendMessageSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField()
    text        = serializers.CharField(max_length=2000)


class ConversationSerializer(serializers.ModelSerializer):
    other_user_id     = serializers.SerializerMethodField()
    other_username    = serializers.SerializerMethodField()
    other_avatar      = serializers.SerializerMethodField()
    last_message_text = serializers.SerializerMethodField()
    last_message_time = serializers.SerializerMethodField()
    unread_count      = serializers.SerializerMethodField()

    class Meta:
        model  = Conversation
        fields = ['id', 'other_user_id', 'other_username', 'other_avatar',
                  'last_message_text', 'last_message_time', 'unread_count', 'updated_at']

    def _other(self, obj):
        me = self.context['request'].user.profile
        return obj.user2 if obj.user1 == me else obj.user1

    def get_other_user_id(self, obj):     return self._other(obj).id
    def get_other_username(self, obj):    return self._other(obj).username
    def get_other_avatar(self, obj):      return self._other(obj).avatar_url
    def get_last_message_text(self, obj): return obj.last_message.text if obj.last_message else ''
    def get_last_message_time(self, obj):
        return obj.last_message.created_at.isoformat() if obj.last_message else ''
    def get_unread_count(self, obj):
        me = self.context['request'].user.profile
        return DirectMessage.objects.filter(
            sender=self._other(obj), receiver=me, is_read=False
        ).count()