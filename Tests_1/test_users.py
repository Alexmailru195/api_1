from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from Tests_1.utils import create_user, get_admin_user, create_member_user
from users.serializers import UserSerializer

# Получаем модель пользователя из Django
User = get_user_model()


class UserTests(APITestCase):
    def setUp(self):
        """
        Настройка тестового окружения:
        - Создаем суперпользователя.
        - Создаем обычного пользователя-участника.
        - Аутентифицируем клиента как суперпользователя по умолчанию.
        """
        self.admin_user = get_admin_user()
        self.member_user = create_member_user(
            username="test1",
            password="test1",
            email="test1@mail.ru"
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_user_list_superuser_access(self):
        """
        Тест: Суперпользователь может получить список всех пользователей.
        """
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Проверяем, что список не пуст

    def test_user_list_member_access_denied(self):
        """
        Тест: Обычному пользователю должно быть отказано в доступе к списку пользователей.
        """
        self.client.force_authenticate(user=self.member_user)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_detail_superuser_access(self):
        """
        Тест: Суперпользователь может получить детали любого пользователя.
        """
        url = reverse('user-detail', args=[self.member_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.member_user.username)
        self.assertEqual(response.data['email'], self.member_user.email)

    def test_user_detail_self_access(self):
        """
        Тест: Пользователь может получить свои собственные детали.
        """
        self.client.force_authenticate(user=self.member_user)
        url = reverse('user-detail', args=[self.member_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.member_user.username)
        self.assertEqual(response.data['email'], self.member_user.email)

    def test_user_detail_other_user_access_denied(self):
        """
        Тест: Пользователь не может получить детали другого пользователя.
        """
        other_user = create_user(
            username="test2",
            password="test2",
            email="test2@mail.ru"
        )
        self.client.force_authenticate(user=self.member_user)
        url = reverse('user-detail', args=[other_user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_serializer(self):
        """
        Тест: Проверка работы сериализатора для создания нового пользователя.
        """
        data = {
            'username': 'test3',
            'email': 'test3@mail.ru',
            'password': 'securepassword123',
            'password2': 'securepassword123'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, 'test3')
        self.assertEqual(user.email, 'test3@mail.ru')
        self.assertTrue(user.check_password('securepassword123'))

    def test_create_user_with_mismatched_passwords(self):
        """
        Тест: Проверка, что сериализатор не позволяет создать пользователя с несовпадающими паролями.
        """
        data = {
            'username': 'test4',
            'email': 'test4@mail.ru',
            'password': 'test4',
            'password2': 'wrong_password'  # Пароли не совпадают
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password2', serializer.errors)  # Проверяем, что ошибка связана с password2

    def test_update_user_as_superuser(self):
        """
        Тест: Суперпользователь может обновить данные пользователя.
        """
        url = reverse('user-detail', args=[self.member_user.pk])
        updated_data = {
            'username': 'updated_username',
            'email': 'updated_test1@mail.ru',
            'password': 'newpassword123',  # Новый пароль
            'password2': 'newpassword123'  # Подтверждение нового пароля
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.member_user.refresh_from_db()
        self.assertEqual(self.member_user.username, 'updated_username')
        self.assertEqual(self.member_user.email, 'updated_test1@mail.ru')
        self.assertTrue(self.member_user.check_password('newpassword123'))

    def test_update_user_as_self(self):
        """
        Тест: Пользователь может обновить свои собственные данные.
        """
        self.client.force_authenticate(user=self.member_user)
        url = reverse('user-detail', args=[self.member_user.pk])
        updated_data = {
            'username': 'updated_username',
            'email': 'updated_test1@mail.ru',
            'password': 'newpassword123',  # Новый пароль
            'password2': 'newpassword123'  # Подтверждение нового пароля
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.member_user.refresh_from_db()
        self.assertEqual(self.member_user.username, 'updated_username')
        self.assertEqual(self.member_user.email, 'updated_test1@mail.ru')
        self.assertTrue(self.member_user.check_password('newpassword123'))

    def test_delete_other_user_denied(self):
        """
        Тест: Пользователь не может удалить аккаунт другого пользователя.
        """
        other_user = create_user(
            username="test5",
            password="test5",
            email="test5@mail.ru"
        )
        self.client.force_authenticate(user=self.member_user)
        url = reverse('user-detail', args=[other_user.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_as_superuser(self):
        """
        Тест: Суперпользователь может удалить пользователя.
        """
        user_to_delete = create_user(
            username="test6",
            password="test6",
            email="test6@mail.ru"
        )
        url = reverse('user-detail', args=[user_to_delete.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=user_to_delete.pk)

    def test_delete_user_as_self(self):
        """
        Тест: Пользователь может удалить свой собственный аккаунт.
        """
        self.client.force_authenticate(user=self.member_user)
        url = reverse('user-detail', args=[self.member_user.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.member_user.pk)

        def test_delete_other_user_denied(self):
            """
            Тест: Пользователь не может удалить аккаунт другого пользователя.
            """
            other_user = create_user(
                username="test5",
                password="test5",
                email="test5@mail.ru"
            )
            self.client.force_authenticate(user=self.member_user)
            url = reverse('user-detail', args=[other_user.pk])
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
