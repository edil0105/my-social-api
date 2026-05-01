from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserProfileViewSet, PostViewSet, MediaViewSet, FollowViewSet,
    LikeViewSet, CommentViewSet, NoteViewSet, StoryViewSet,
    RegisterView, FeedView, ConversationListView, ChatView
)

router = DefaultRouter()
router.register(r'users',    UserProfileViewSet)
router.register(r'posts',    PostViewSet)
router.register(r'media',    MediaViewSet)
router.register(r'follows',  FollowViewSet)
router.register(r'likes',    LikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'notes',    NoteViewSet)
router.register(r'stories',  StoryViewSet, basename='story')

urlpatterns = [
    path('', include(router.urls)),
    path('token/',                   TokenObtainPairView.as_view()),
    path('token/refresh/',           TokenRefreshView.as_view()),
    path('register/',                RegisterView.as_view()),
    path('feed/',                    FeedView.as_view()),
    path('conversations/',           ConversationListView.as_view()),
    path('chat/<int:user_id>/',      ChatView.as_view()),
]