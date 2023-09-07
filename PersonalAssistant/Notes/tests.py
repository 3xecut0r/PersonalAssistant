from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from Notes.models import Tag  # Импортируйте модели, если не сделали это ранее


class TagViewTestCase(TestCase):
    def setUp(self):
        # Создайте тестового пользователя для использования в тестах
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = Client()  # Создайте клиента для имитации HTTP запросов

    def test_tag_view_get(self):
        # Создайте тестовый GET запрос к вашей вью
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("notes:add-tags"))

        # Проверьте, что ответ имеет статус 200 (ОК)
        self.assertEqual(response.status_code, 200)

    def test_tag_view_without_login(self):
        response = self.client.get(reverse("notes:add-tags"))
        self.assertEqual(
            response.status_code, 302
        )  # ожидаем редирект, так как не авторизовались
        self.assertTrue(
            response.url.startswith(reverse("login"))
        )  # перенаправление на страницу входа

    def test_tag_view_with_invalid_post_data(self):
        self.client.login(username="testuser", password="testpassword")
        data = {}  # отправляем пустые данные, что неверно
        response = self.client.post(reverse("notes:add-tags"), data)
        self.assertEqual(
            response.status_code, 200
        )  # Ожидаем ответ с кодом 200, так как форма неверна и мы возвращаемся на ту же страницу
        self.assertContains(
            response, "This field is required."
        )  # проверяем, что на странице есть сообщение об ошибке

    def test_tag_view_post(self):
        # Создайте тестовый POST запрос к вашей вью
        self.client.login(username="testuser", password="testpassword")
        data = {"name": "Test Tag"}  # Параметры для POST запроса
        response = self.client.post(reverse("notes:add-tags"), data)

        # Проверьте, что после POST запроса произошло перенаправление (редирект)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("notes:index"))

        # Проверьте, что тег был создан в базе данных
        self.assertTrue(Tag.objects.filter(name="Test Tag", user=self.user).exists())
