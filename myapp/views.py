from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import (
    UserProfile, Post, Media, Follow, 
    Like, Comment, RefreshToken, Note, Story
)
from .serializers import (
    UserProfileSerializer, PostSerializer, MediaSerializer, 
    FollowSerializer, LikeSerializer, CommentSerializer, 
    RefreshTokenSerializer, NoteSerializer, StorySerializer
)

# 1. Пайдаланушы профилі
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

# 2. Посттар
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

# 3. Медиа файлдар
class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]

# 4. Жазылулар (Follows)
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

# 5. Лайктар
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

# 6. Пікірлер
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

# 7. Заметки (Notes)
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]  # Тек тіркелгендер көре алуы үшін

# 8. Историялар (Stories)
class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]

# 9. Refresh Tokens
class RefreshTokenViewSet(viewsets.ModelViewSet):
    queryset = RefreshToken.objects.all()
    serializer_class = RefreshTokenSerializer
    permission_classes = [IsAuthenticated]