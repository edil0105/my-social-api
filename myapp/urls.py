from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Барлық ViewSet-терді нақты импорттау
from .views import (
    UserProfileViewSet, PostViewSet, MediaViewSet, 
    FollowViewSet, LikeViewSet, CommentViewSet, 
    RefreshTokenViewSet, NoteViewSet, StoryViewSet
)

# Роутерді баптау
router = DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'posts', PostViewSet)
router.register(r'media', MediaViewSet)
router.register(r'follows', FollowViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'refresh-tokens', RefreshTokenViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'stories', StoryViewSet)

# URL жолдары
urlpatterns = [
    # API-дің басты беті (Api Root) және барлық ресурстар
    path('', include(router.urls)),
    
    # JWT Аутентификация токендері
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
from .views import create_admin_fix # views-тан импортта

urlpatterns = [
    path('fix-admin/', create_admin_fix), # Осы жолды қос
    # ... қалғандары тұра берсін
]