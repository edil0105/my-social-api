from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.utils import timezone

from .models import UserProfile, Post, Media, Follow, Like, Comment, Note, Story
from .serializers import (
    UserProfileSerializer, PostSerializer, MediaSerializer,
    FollowSerializer, LikeSerializer, CommentSerializer,
    NoteSerializer, StorySerializer, RegisterSerializer, SearchUserSerializer
)


# ── 1. ТІРКЕЛУ ──────────────────────────────────────────────────────────────
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        username = serializer.validated_data['username']
        email    = serializer.validated_data['email']
        password = serializer.validated_data['password']

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Бұл username бос емес'}, status=400)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Бұл email тіркелген'}, status=400)

        user    = User.objects.create_user(username=username, email=email, password=password)
        profile = UserProfile.objects.create(user=user, username=username, email=email, password_hash='')
        return Response({'message': 'Тіркелу сәтті өтті!', 'user_id': profile.id}, status=201)


# ── 2. ЛЕНТА ─────────────────────────────────────────────────────────────────
class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return Response({'error': 'Профиль табылмады'}, status=404)

        following_ids = Follow.objects.filter(follower=profile).values_list('followee_id', flat=True)
        posts = Post.objects.filter(
            author_id__in=list(following_ids) + [profile.id]
        ).order_by('-created_at')

        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


# ── 3. ПАЙДАЛАНУШЫЛАР ─────────────────────────────────────────────────────────
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'bio']

    # GET /api/users/me/
    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return Response({'error': 'Профиль жоқ'}, status=404)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return SearchUserSerializer
        return UserProfileSerializer


# ── 4. ПОСТТАР ───────────────────────────────────────────────────────────────
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
        post = serializer.save(author=profile)

        # image_url болса, Media жазбасын автоматты жасау
        image_url = self.request.data.get('image_url', '')
        if image_url:
            Media.objects.create(
                post=post,
                url=image_url,
                mime_type='image/jpeg',
                order_idx=0
            )


# ── 5. МЕДИА ─────────────────────────────────────────────────────────────────
class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]


# ── 6. ЖАЗЫЛУЛАР ─────────────────────────────────────────────────────────────
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


# ── 7. ЛАЙКТАР ───────────────────────────────────────────────────────────────
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Like.objects.all()
        post_id = self.request.query_params.get('post')
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        try:
            profile = self.request.user.profile
        except UserProfile.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Профиль жоқ')
        serializer.save(user=profile)


# ── 8. ПІКІРЛЕР ───────────────────────────────────────────────────────────────
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Comment.objects.all()
        post_id = self.request.query_params.get('post')
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs.order_by('created_at')

    def perform_create(self, serializer):
        try:
            profile = self.request.user.profile
        except UserProfile.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Профиль жоқ')
        serializer.save(author=profile)


# ── 9. ЗАМЕТКИ ────────────────────────────────────────────────────────────────
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]


# ── 10. СТОРИС ───────────────────────────────────────────────────────────────
class StoryViewSet(viewsets.ModelViewSet):
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Тек белсенді (24 сағат өтпеген) сторис-тарды қайтару
        return Story.objects.filter(expires_at__gt=timezone.now()).order_by('-created_at')