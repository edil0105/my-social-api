from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'posts', PostViewSet)
router.register(r'media', MediaViewSet)
router.register(r'follows', FollowViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'refresh-tokens', RefreshTokenViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]