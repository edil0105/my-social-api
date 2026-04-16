from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from .models import (
    UserProfile, Post, Media, Follow,
    Like, Comment, Note, Story
)
from .serializers import (
    UserProfileSerializer, PostSerializer, MediaSerializer,
    FollowSerializer, LikeSerializer, CommentSerializer,
    NoteSerializer, StorySerializer, RegisterSerializer
)


# 1. Тіркелу (Register)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Бұл username бос емес'}, status=400)
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Бұл email тіркелген'}, status=400)

            user = User.objects.create_user(username=username, email=email, password=password)
            profile = UserProfile.objects.create(
                user=user,
                username=username,
                email=email,
                password_hash=''  # Django User-де сақталады
            )
            return Response({'message': 'Тіркелу сәтті өтті!', 'user_id': profile.id}, status=201)

        return Response(serializer.errors, status=400)


# 2. Лента (Feed) — жазылғандардың посттары
class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return Response({'error': 'Профиль табылмады'}, status=404)

        # Кімге жазылған соларды табу
        following_ids = Follow.objects.filter(follower=profile).values_list('followee_id', flat=True)

        # Өзінің де, жазылғандардың да посттары
        posts = Post.objects.filter(
            author_id__in=list(following_ids) + [profile.id]
        ).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


# 3. Пайдаланушы профилі
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


# 4. Посттар
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            profile = self.request.user.profile
        except UserProfile.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Профиль жоқ')
        serializer.save(author=profile)


# 5. Медиа
class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]


# 6. Жазылулар (Follow)
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]


# 7. Лайктар
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]


# 8. Пікірлер
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


# 9. Заметки
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]


# 10. Сторис
class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]