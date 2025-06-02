from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class ConfigTests(APITestCase):
    def setUp(self):
        """
        Настройка тестового окружения:
        - Создаем суперпользователя.
        """
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="adminpassword",
            email="admin@example.com"
        )

    def test_swagger_ui_accessible(self):
        """
        Тест: Swagger UI доступен по своему URL.
        """
        url = reverse('schema-swagger-ui')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_redoc_ui_accessible(self):
        """
        Тест: ReDoc UI доступен по своему URL.
        """
        url = reverse('schema-redoc')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_obtain_pair_accessible(self):
        """
        Тест: Эндпоинт для получения токена доступен только для POST-запросов.
        """
        url = reverse('token_obtain_pair')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_token_refresh_accessible(self):
        """
        Тест: Эндпоинт для обновления токена доступен только для POST-запросов.
        """
        url = reverse('token_refresh')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_root_accessible(self):
        """
        Тест: Корневой API-эндпоинт доступен для GET-запросов.
        """
        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.admin_user)

        # Получаем URL для корневого API
        url = reverse('api-root')

        # Выполняем GET-запрос к корневому API
        response = self.client.get(url)

        # Проверяем, что страница доступна (статус 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
