from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserList, UserDetail

# Создаем роутер для автоматической генерации URL-маршрутов
router = DefaultRouter()
router.register(r'users', UserViewSet)

# Определяем urlpatterns с поддержкой как DefaultRouter, так и ручных маршрутов
urlpatterns = [
    # Автоматические маршруты через DefaultRouter
    path('', include(router.urls)),

    # Ручные маршруты для UserList и UserDetail
    path('api/users/', UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]
