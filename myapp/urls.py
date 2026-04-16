from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserProfileViewSet, PostViewSet, MediaViewSet,
    FollowViewSet, LikeViewSet, CommentViewSet,
    NoteViewSet, StoryViewSet,
    RegisterView, FeedView
)

router = DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'posts', PostViewSet)
router.register(r'media', MediaViewSet)
router.register(r'follows', FollowViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'stories', StoryViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # JWT токендер — Login осы арқылы жасалады
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Тіркелу (Register)
    path('register/', RegisterView.as_view(), name='register'),

    # Лента (Feed) — тек өзің жазылғандардың посттары
    path('feed/', FeedView.as_view(), name='feed'),
]