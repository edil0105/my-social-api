from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class UserProfile(models.Model):
    user          = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username      = models.CharField(max_length=32, unique=True)
    email         = models.EmailField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255, blank=True)
    bio           = models.TextField(null=True, blank=True)
    avatar_url    = models.CharField(max_length=512, null=True, blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    author     = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    caption    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Media(models.Model):
    post      = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    url       = models.CharField(max_length=512)
    mime_type = models.CharField(max_length=64, default='image/jpeg')
    width     = models.IntegerField(default=0)
    height    = models.IntegerField(default=0)
    order_idx = models.IntegerField(default=0)


class Follow(models.Model):
    follower   = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE)
    followee   = models.ForeignKey(UserProfile, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followee')


class Like(models.Model):
    user       = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='likes')
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ✅ 1 пайдаланушы — 1 постқа тек 1 лайк
        unique_together = ('user', 'post')


class Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author     = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class Note(models.Model):
    user       = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notes')
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


def get_story_expiry():
    return timezone.now() + timedelta(hours=24)


class Story(models.Model):
    user       = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='stories')
    # ✅ ImageField емес — URL string (Cloudinary/imgbb сілтемесі)
    image      = models.CharField(max_length=512, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_story_expiry)

    class Meta:
        ordering = ['-created_at']


class DirectMessage(models.Model):
    sender     = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver   = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    text       = models.TextField()
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class Conversation(models.Model):
    user1        = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='conversations_as_user1')
    user2        = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='conversations_as_user2')
    last_message = models.ForeignKey(DirectMessage, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user1', 'user2')
        ordering = ['-updated_at']