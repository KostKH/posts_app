from django.contrib.auth import get_user_model
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomObtainAuthToken, PostViewSet, UserCreateView,
                    UserListViewSet, UserPostsView)

User = get_user_model()

router = DefaultRouter()
router.register('users', UserListViewSet, basename='api-user')
router.register('posts', PostViewSet, basename='api-post')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', UserCreateView.as_view(), name='api-signup'),
    path('auth/login/', CustomObtainAuthToken.as_view(), name='api-login'),
    path('users/<int:id>/posts/',
         UserPostsView.as_view(),
         name='api-user-posts'),
]
