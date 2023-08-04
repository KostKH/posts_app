from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import AllowAny, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from posts.models import Post

from .serializers import (CustomAuthTokenSerializer, PostSerializer,
                          UserCreateSerializer, UserSerializer)

User = get_user_model()


class UserListViewSet(ListModelMixin, GenericViewSet):
    """Класс для обработки эндпойнта на вывод списка пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserCreateView(APIView):
    """Класс для обработки эндпойнта на создание пользователя."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(ObtainAuthToken):
    """Класс для обработки эндпойнта создания токена авторизации."""

    serializer_class = CustomAuthTokenSerializer


class PostViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, serializer):
        if serializer.user != self.request.user:
            raise exceptions.PermissionDenied(
                'Изменение чужого контента запрещено!'
            )
        super(PostViewSet, self).perform_destroy(serializer)


class UserPostsView(ListAPIView):

    serializer_class = PostSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        return user.posts.all()
