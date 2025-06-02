from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .permissions import IsSuperUser, IsSelf
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


@api_view(['GET'])
def api_root(request):
    """
    Корневой API-эндпоинт.
    """
    return Response({
        'users': reverse('user-list', request=request),
        'sections': reverse('section-list-create', request=request),
    })


# Разрешаем доступ без аутентификации
api_root.permission_classes = [AllowAny]


class UserList(generics.ListCreateAPIView):
    """
    API endpoint для получения списка пользователей или создания нового пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]

    def get(self, request, *args, **kwargs):
        logger.debug(f"Authorization header: {request.META.get('HTTP_AUTHORIZATION')}")
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint для получения, обновления или удаления конкретного пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelf]

    def get_object(self):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)
        if not self.request.user == user and not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to access this user's profile.")
        return user

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return Response({"detail": "Failed to delete user."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
