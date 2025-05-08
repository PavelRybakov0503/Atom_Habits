from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class RegistrationApiViewTest(APITestCase):
    """
    Тесты для API регистрации пользователя.
    """

    def setUp(self):
        """
        Настройка перед каждым тестом.
        """
        pass

    def test_registration_api_view(self):
        """
        Проверяет успешную регистрацию нового пользователя через API.
        Отправляет POST-запрос на эндпоинт регистрации и проверяет, что пользователь создан.
        """
        registration_data = {
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        response = self.client.post('/users/register/', registration_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="testuser@example.com")
        self.assertIsNotNone(user)

    def tearDown(self):
        """
        Очистка после выполнения теста.
        """
        pass
