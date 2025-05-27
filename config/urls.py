from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import redirect

# Настройка Swagger/OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="API управления профилями пользователей",
        default_version='v1',
        description="Этот API предоставляет конечные точки для управления профилями пользователей.",
        terms_of_service="https://www.anim.example.com/terms/ ",  # Убран лишний пробел в конце
        contact=openapi.Contact(email="api-support@anim.example.com"),
        license=openapi.License(name="Лицензия MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Разрешить доступ всем пользователям
)

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # JWT аутентификация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Пользователи
    path('api/users/', include('users.urls')),

    # Документация API
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Разделы и тесты
    path('api/sections/', include('sections.urls')),  # Маршруты для разделов
    path('api/quiz/', include('quiz.urls')),          # Маршруты для тестов

    # Корневой URL
    path('', lambda request: redirect('schema-swagger-ui')),  # Перенаправление на Swagger UI

    # Маршруты для аутентификации
    path('accounts/', include('django.contrib.auth.urls')),  # Стандартные маршруты для входа/выхода
]