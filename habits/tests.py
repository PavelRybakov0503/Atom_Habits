from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import HealthyHabit, PleasantHabit
from users.models import User


# Create your tests here.
class HabitTestCase(APITestCase):
    """
    Набор тестов для проверки API по управлению привычками (HealthyHabit, PleasantHabit).

    Тестирует основной CRUD-функционал для обеих моделей привычек.
    """

    def setUp(self):
        """
        Создаёт тестового пользователя и выполняет принудительную аутентификацию для API-клиента.
        """
        self.user = User.objects.create(
            email='testuser@gmail.com',
        )
        self.user.set_password('testpassword')
        self.client.force_authenticate(user=self.user)

    def test_healthy_habit(self):
        """
        Проверяет создание, получение списка, просмотр, обновление и удаление полезной привычки через API.
        """
        data = {
            "place": "Дом",
            "time": "10:00",
            "action": "Учить",
            "time_required": 115,
            "reward": "5 долларов",
        }

        response = self.client.post(
            '/habits/healthy_habits/create',
            data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        response = self.client.get('/habits/healthy_habits')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        response = self.client.get(f'/habits/healthy_habits/{HealthyHabit.objects.all().first().pk}')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        data = {
            'place': 'Улица'
        }

        response = self.client.patch(
            f'/habits/healthy_habits/update/{HealthyHabit.objects.all().first().pk}',
            data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        response = self.client.delete(
            f'/habits/healthy_habits/delete/{HealthyHabit.objects.all().first().pk}',
            data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_pleasant_habit(self):
        """
        Проверяет создание, получение списка, просмотр, обновление и удаление приятной привычки через API.
        """
        data = {
            "place": "Улица",
            "time": "12:00",
            "action": "Играть",
            "time_required": 100,
        }

        response = self.client.post(
            '/habits/pleasant_habits/create',
            data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        response = self.client.get('/habits/pleasant_habits')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        response = self.client.get(f'/habits/pleasant_habits/{PleasantHabit.objects.all().first().pk}')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        data = {
            'place': 'Дом'
        }

        response = self.client.patch(
            f'/habits/pleasant_habits/update/{PleasantHabit.objects.all().first().pk}',
            data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        response = self.client.delete(
            f'/habits/pleasant_habits/delete/{PleasantHabit.objects.all().first().pk}',
            data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
from django.test import TestCase

# Create your tests here.
