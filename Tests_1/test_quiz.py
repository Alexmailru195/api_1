import logging

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from Tests_1.utils import get_admin_user, create_member_user
from quiz.models import QuestionCategory, Question, Answer

# Получаем модель пользователя из Django
User = get_user_model()

# Настройка логирования
logger = logging.getLogger(__name__)


class QuizTests(APITestCase):
    def setUp(self):
        """
        Настройка тестового окружения:
        - Создаем суперпользователя.
        - Создаем обычного пользователя-участника.
        """
        logger.debug("Настройка тестового окружения...")
        self.admin_user = get_admin_user()
        self.member_user = create_member_user(
            username="member_test",
            password="password123",
            email="member@example.com"
        )

    def test_check_answer_correct(self):
        """
        Тест: Проверка правильного ответа на вопрос.
        """
        # Создаем категорию, вопрос и правильный ответ
        category = QuestionCategory.objects.create(name="Test Category")
        question = Question.objects.create(category=category, text="Test Question", difficulty="easy")
        correct_answer = Answer.objects.create(question=question, text="Correct Answer", is_correct=True)

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.member_user)

        # Отправляем запрос на проверку ответа
        url = reverse('check_answer')
        data = {'question_id': question.pk, 'answer_id': correct_answer.pk}
        response = self.client.post(url, data)

        # Проверяем результат
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_correct'], True)
        self.assertEqual(response.data['question_text'], question.text)

    def test_check_answer_incorrect(self):
        """
        Тест: Проверка неправильного ответа на вопрос.
        """
        # Создаем категорию, вопрос и неправильный ответ
        category = QuestionCategory.objects.create(name="Test Category")
        question = Question.objects.create(category=category, text="Test Question", difficulty="easy")
        incorrect_answer = Answer.objects.create(question=question, text="Incorrect Answer", is_correct=False)

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.member_user)

        # Отправляем запрос на проверку ответа
        url = reverse('check_answer')
        data = {'question_id': question.pk, 'answer_id': incorrect_answer.pk}
        response = self.client.post(url, data)

        # Проверяем результат
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_correct'], False)
        self.assertEqual(response.data['question_text'], question.text)

    def test_check_answer_question_not_found(self):
        """
        Тест: Проверка ответа на несуществующий вопрос.
        """
        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.member_user)

        # Отправляем запрос на проверку ответа с несуществующим вопросом
        url = reverse('check_answer')
        data = {'question_id': 999, 'answer_id': 1}
        response = self.client.post(url, data)

        # Проверяем результат
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_check_answer_answer_not_found(self):
        """
        Тест: Проверка ответа с несуществующим вариантом ответа.
        """
        # Создаем категорию и вопрос
        category = QuestionCategory.objects.create(name="Test Category")
        question = Question.objects.create(category=category, text="Test Question", difficulty="easy")

        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.member_user)

        # Отправляем запрос на проверку ответа с несуществующим вариантом ответа
        url = reverse('check_answer')
        data = {'question_id': question.pk, 'answer_id': 999}
        response = self.client.post(url, data)

        # Проверяем результат
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_question_category_list_create(self):
        """
        Тест: Создание и получение списка категорий вопросов.
        """
        # Аутентифицируем суперпользователя
        self.client.force_authenticate(user=self.admin_user)

        # URL для создания и получения категорий
        url = reverse('category-list-create')

        # Создаем новую категорию
        data = {'name': 'New Category'}
        response_post = self.client.post(url, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

        # Получаем список категорий
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), 1)
        self.assertEqual(response_get.data[0]['name'], 'New Category')

    def test_question_category_detail(self):
        """
        Тест: Получение деталей категории.
        """
        # Создаем категорию
        category = QuestionCategory.objects.create(name="Test Category")

        # Аутентифицируем суперпользователя
        self.client.force_authenticate(user=self.admin_user)

        # URL для получения деталей категории
        url = reverse('category-detail', args=[category.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], category.name)

    def test_question_category_update(self):
        """
        Тест: Обновление категории.
        """
        # Создаем категорию
        category = QuestionCategory.objects.create(name="Old Name")

        # Аутентифицируем суперпользователя
        self.client.force_authenticate(user=self.admin_user)

        # URL для обновления категории
        url = reverse('category-detail', args=[category.pk])
        updated_data = {'name': 'New Name'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, 'New Name')

    def test_question_category_delete(self):
        """
        Тест: Удаление категории.
        """
        # Создаем категорию
        category = QuestionCategory.objects.create(name="Test Category")

        # Аутентифицируем суперпользователя
        self.client.force_authenticate(user=self.admin_user)

        # URL для удаления категории
        url = reverse('category-detail', args=[category.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(QuestionCategory.objects.filter(pk=category.pk).exists())
