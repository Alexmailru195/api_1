from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from Tests_1.utils import get_admin_user, create_member_user
from sections.models import Section

# Получаем модель пользователя из Django
User = get_user_model()


class SectionTests(APITestCase):
    def setUp(self):
        """
        Настройка тестового окружения:
        - Создаем суперпользователя.
        - Создаем обычного пользователя-участника.
        - Создаем две секции: одну принадлежащую участнику, другую — суперпользователю.
        """
        self.admin_user = get_admin_user()
        self.member_user = create_member_user(
            username="member_test",
            password="password123",
            email="member@example.com"
        )

        # Создаем секции
        self.section1 = Section.objects.create(title="Section 1", owner=self.member_user)
        self.section2 = Section.objects.create(title="Section 2", owner=self.admin_user)

    def test_section_list_access(self):
        """
        Тест: Пользователь может видеть только свои секции в списке.
        """
        self.client.force_authenticate(user=self.member_user)
        url = reverse('section-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Только одна секция принадлежит member_user
        self.assertEqual(response.data['results'][0]['title'], self.section1.title)

    def test_section_create_access(self):
        """
        Тест: Пользователь может создать новую секцию.
        """
        self.client.force_authenticate(user=self.member_user)
        url = reverse('section-list-create')
        data = {'title': 'New Section'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Section.objects.count(), 3)
        self.assertEqual(Section.objects.last().owner, self.member_user)

    def test_section_detail_owner_access(self):
        """
        Тест: Пользователь может получить детали своей секции.
        """
        self.client.force_authenticate(user=self.member_user)
        url = reverse('section-detail', args=[self.section1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.section1.title)

    def test_section_detail_other_user_access_denied(self):
        """
        Тест: Пользователь не может получить детали чужой секции.
        """
        self.client.force_authenticate(user=self.member_user)
        url = reverse('section-detail', args=[self.section2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_section_update_owner_access(self):
        """
        Тест: Пользователь может обновить свою секцию.
        """
        self.client.force_authenticate(user=self.member_user)
        url = reverse('section-detail', args=[self.section1.pk])
        updated_data = {'title': 'Updated Section Title'}
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.section1.refresh_from_db()
        self.assertEqual(self.section1.title, 'Updated Section Title')

    def test_section_update_other_user_access_denied(self):
        """
        Тест: Пользователь не может обновить чужую секцию.
        """
        self.client.force_authenticate(user=self.member_user)
        url = reverse('section-detail', args=[self.section2.pk])
        updated_data = {'title': 'Updated Section Title'}
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_section_delete_owner_access(self):
        """
        Тест: Пользователь может удалить свою секцию.
        """
        self.client.force_authenticate(user=self.member_user)
        url = reverse('section-detail', args=[self.section1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Section.objects.count(), 1)

    def test_section_delete_other_user_access_denied(self):
        """
        Тест: Пользователь не может удалить чужую секцию.
        """
        self.client.force_authenticate(user=self.member_user)
        url = reverse('section-detail', args=[self.section2.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
