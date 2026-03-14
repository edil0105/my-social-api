from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# 1. Қолданушы профилі (Users)
# Бұл модель стандартты Django User-імен бірге жасалады
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255) # Ескерту: Django мұны 'user' ішінде өзі сақтайды
    bio = models.TextField(null=True, blank=True)
    avatar_url = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# 2. Посттар (Posts)
class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"

# 3. Медиа файлдар (Media)
class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    url = models.CharField(max_length=512)
    mime_type = models.CharField(max_length=64)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    order_idx = models.IntegerField(default=0)

# 4. Жазылулар (Follows)
class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE)
    followee = models.ForeignKey(UserProfile, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followee') # Бір адамға екі рет жазылуды болдырмау

# 5. Лайктар (Likes)
class Like(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

# 6. Пікірлер (Comments)
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 7. Заметки (Notes)
class Note(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.user.username}"

# 8. Историялар (Stories)
def get_story_expiry():
    return timezone.now() + timedelta(hours=24)

class Story(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='stories')
    image = models.ImageField(upload_to='stories/')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_story_expiry)

    def is_active(self):
        return timezone.now() < self.expires_at

    class Meta:
        verbose_name_plural = "Stories"

# 9. Refresh Tokens (Егер SimpleJWT қолдансаң, бұл модель міндетті емес, бірақ сақтауға болады)
class RefreshToken(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    jti = models.CharField(max_length=64, unique=True)
    revoked = models.BooleanField(default=False)
    expires_at = models.DateTimeField()