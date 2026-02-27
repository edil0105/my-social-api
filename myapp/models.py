from django.db import models
from django.contrib.auth.models import User

# 1. Қолданушы профилі (Users)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    avatar_url = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# 2. Посттар (Posts)
class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 3. Медиа файлдар (Media)
class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.CharField(max_length=512)
    mime_type = models.CharField(max_length=64)
    width = models.IntegerField()
    height = models.IntegerField()
    order_idx = models.IntegerField()

# 4. Жазылулар (Follows)
class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE)
    followee = models.ForeignKey(UserProfile, related_name='followers', on_delete=models.CASCADE)

# 5. Лайктар (Likes)
class Like(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# 6. Пікірлер (Comments)
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 7. Refresh Tokens
class RefreshToken(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    jti = models.CharField(max_length=64, unique=True)
    revoked = models.BooleanField(default=False)
    expires_at = models.DateTimeField()