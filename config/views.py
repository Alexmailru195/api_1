from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .permissions import IsSuperUser, IsSelf
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]

    def get(self, request, *args, **kwargs):
        logger.debug(f"Authorization header: {request.META.get('HTTP_AUTHORIZATION')}")
        return super().get(request, *args, **kwargs)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelf]