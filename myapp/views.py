from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User

from .models import (
    UserProfile, Post, Media, Follow, Like,
    Comment, Note, Story, DirectMessage, Conversation
)
from .serializers import (
    UserProfileSerializer, PostSerializer, MediaSerializer,
    FollowSerializer, LikeSerializer, CommentSerializer,
    NoteSerializer, StorySerializer, RegisterSerializer,
    SearchUserSerializer, DirectMessageSerializer,
    SendMessageSerializer, ConversationSerializer
)


# ── 1. Тіркелу ──────────────────────────────────────────────────────────────
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=400)
        u, e, p = s.validated_data['username'], s.validated_data['email'], s.validated_data['password']
        if User.objects.filter(username=u).exists():
            return Response({'error': 'Бұл username бос емес'}, status=400)
        if User.objects.filter(email=e).exists():
            return Response({'error': 'Бұл email тіркелген'}, status=400)
        user    = User.objects.create_user(username=u, email=e, password=p)
        profile = UserProfile.objects.create(user=user, username=u, email=e, password_hash='')
        return Response({'message': 'Тіркелу сәтті!', 'user_id': profile.id}, status=201)


# ── 2. Лента ────────────────────────────────────────────────────────────────
class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return Response({'error': 'Профиль жоқ'}, status=404)
        following_ids = Follow.objects.filter(follower=profile).values_list('followee_id', flat=True)
        posts = Post.objects.filter(
            author_id__in=list(following_ids) + [profile.id]
        ).prefetch_related('media', 'post_likes', 'comments').select_related('author')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


# ── 3. Пайдаланушылар ───────────────────────────────────────────────────────
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset           = UserProfile.objects.all()
    serializer_class   = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [filters.SearchFilter]
    search_fields      = ['username', 'bio']

    def get_serializer_class(self):
        if self.action == 'list':
            return SearchUserSerializer
        return UserProfileSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return Response({'error': 'Профиль жоқ'}, status=404)
        return Response(UserProfileSerializer(profile, context={'request': request}).data)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """GET /api/users/{id}/posts/ — профиль беттегі посттар"""
        try:
            profile = UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Пайдаланушы жоқ'}, status=404)
        posts = Post.objects.filter(author=profile).prefetch_related('media', 'post_likes')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


# ── 4. Посттар ──────────────────────────────────────────────────────────────
class PostViewSet(viewsets.ModelViewSet):
    queryset           = Post.objects.all().prefetch_related('media', 'post_likes', 'comments').select_related('author')
    serializer_class   = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        try:
            profile = self.request.user.profile
        except UserProfile.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Профиль жоқ')
        post = serializer.save(author=profile)
        # image_url болса Media автоматты жасалады
        image_url = self.request.data.get('image_url', '').strip()
        if image_url:
            Media.objects.create(post=post, url=image_url, mime_type='image/jpeg', order_idx=0)
        return post


# ── 5. Медиа ────────────────────────────────────────────────────────────────
class MediaViewSet(viewsets.ModelViewSet):
    queryset           = Media.objects.all()
    serializer_class   = MediaSerializer
    permission_classes = [IsAuthenticated]


# ── 6. Жазылулар ────────────────────────────────────────────────────────────
class FollowViewSet(viewsets.ModelViewSet):
    queryset           = Follow.objects.all()
    serializer_class   = FollowSerializer
    permission_classes = [IsAuthenticated]


# ── 7. Лайктар — 1 пайдаланушы 1 постқа 1 рет ─────────────────────────────
class LikeViewSet(viewsets.ModelViewSet):
    queryset           = Like.objects.all()
    serializer_class   = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs      = Like.objects.all()
        post_id = self.request.query_params.get('post')
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def create(self, request, *args, **kwargs):
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return Response({'error': 'Профиль жоқ'}, status=400)

        post_id = request.data.get('post')
        if not post_id:
            return Response({'error': 'post id жоқ'}, status=400)

        # Бұрын лайк басылған болса қайтарамыз
        existing = Like.objects.filter(user=profile, post_id=post_id).first()
        if existing:
            return Response(LikeSerializer(existing).data, status=200)

        like = Like.objects.create(user=profile, post_id=post_id)
        return Response(LikeSerializer(like).data, status=201)

    def destroy(self, request, *args, **kwargs):
        """Лайкты алып тастау"""
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return Response({'error': 'Профиль жоқ'}, status=400)
        like = self.get_object()
        if like.user != profile:
            return Response({'error': 'Рұқсат жоқ'}, status=403)
        like.delete()
        return Response(status=204)


# ── 8. Пікірлер ─────────────────────────────────────────────────────────────
class CommentViewSet(viewsets.ModelViewSet):
    queryset           = Comment.objects.all()
    serializer_class   = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs      = Comment.objects.all()
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


# ── 9. Stories ───────────────────────────────────────────────────────────────
class StoryViewSet(viewsets.ModelViewSet):
    serializer_class   = StorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Story.objects.filter(expires_at__gt=timezone.now()).select_related('user')

    def perform_create(self, serializer):
        try:
            profile = self.request.user.profile
        except UserProfile.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Профиль жоқ')
        serializer.save(user=profile)


# ── 10. Notes ────────────────────────────────────────────────────────────────
class NoteViewSet(viewsets.ModelViewSet):
    queryset           = Note.objects.all()
    serializer_class   = NoteSerializer
    permission_classes = [IsAuthenticated]


# ── 11. Direct Message ───────────────────────────────────────────────────────
class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            me = request.user.profile
        except UserProfile.DoesNotExist:
            return Response({'error': 'Профиль жоқ'}, status=404)
        convs = Conversation.objects.filter(Q(user1=me) | Q(user2=me)).select_related(
            'user1', 'user2', 'last_message'
        )
        return Response(ConversationSerializer(convs, many=True, context={'request': request}).data)


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def _conv(self, me, other):
        u1, u2 = (me, other) if me.id < other.id else (other, me)
        conv, _ = Conversation.objects.get_or_create(user1=u1, user2=u2)
        return conv

    def get(self, request, user_id):
        try:
            me    = request.user.profile
            other = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Пайдаланушы жоқ'}, status=404)

        # Оқылды деп белгілеу
        DirectMessage.objects.filter(sender=other, receiver=me, is_read=False).update(is_read=True)

        msgs = DirectMessage.objects.filter(
            Q(sender=me, receiver=other) | Q(sender=other, receiver=me)
        ).order_by('created_at')

        return Response({
            'other_user': {'id': other.id, 'username': other.username, 'avatar_url': other.avatar_url},
            'messages':   DirectMessageSerializer(msgs, many=True).data
        })

    def post(self, request, user_id):
        try:
            me    = request.user.profile
            other = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Пайдаланушы жоқ'}, status=404)

        s = SendMessageSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=400)

        msg  = DirectMessage.objects.create(sender=me, receiver=other, text=s.validated_data['text'])
        conv = self._conv(me, other)
        conv.last_message = msg
        conv.save()
        return Response(DirectMessageSerializer(msg).data, status=201)