from django.test import TestCase


class BasicTest(TestCase):
    """
    Класс для базовых тестов.
    Содержит простые проверки для демонстрации работы unittest.
    """

    def test_basic_equality(self):
        """
        Тест: Проверка базового равенства.
        """
        # Проверяем, что 1 равно 1
        self.assertEqual(1, 1)

    def test_basic_truthiness(self):
        """
        Тест: Проверка истинности значения.
        """
        # Проверяем, что значение True является истинным
        self.assertTrue(True)

    def test_basic_falsiness(self):
        """
        Тест: Проверка ложности значения.
        """
        # Проверяем, что значение False является ложным
        self.assertFalse(False)

    def test_basic_addition(self):
        """
        Тест: Проверка сложения двух чисел.
        """
        # Проверяем, что 2 + 2 = 4
        self.assertEqual(2 + 2, 4)

    def test_basic_string_concatenation(self):
        """
        Тест: Проверка конкатенации строк.
        """
        # Проверяем, что "Hello, " + "World!" = "Hello, World!"
        self.assertEqual("Hello, " + "World!", "Hello, World!")

    def test_basic_list_operations(self):
        """
        Тест: Проверка операций со списками.
        """
        # Создаем список
        test_list = [1, 2, 3]

        # Проверяем длину списка
        self.assertEqual(len(test_list), 3)

        # Проверяем, что элементы находятся в списке
        self.assertIn(2, test_list)
        self.assertNotIn(4, test_list)
