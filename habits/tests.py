from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            user=self.user,
            place="test_place",
            time="00:00",
            action="test_action",
            reward="reward",
            time_to_complete=120,
        )

    def test_create_habit(self):
        """Тестирование создания привычки"""

        data = {
            "place": "test_place",
            "time": "00:00",
            "action": "test_action",
            "reward": "reward",
            "time_to_complete": 120,
        }
        response = self.client.post("/habits/create/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_habit(self):
        """Тестирование обновления привычки"""
        data = {
            "place": "update_place",
            "time": "10:00",
            "reward": "reward",
            "pleasant_habit": False,
            "periodicity": 2,
            "time_to_complete": 120,
        }
        response = self.client.patch(f"/habits/{self.habit.pk}/update/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_habits(self):
        """Тестирование получения списка привычек"""
        response = self.client.get("/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_habit(self):
        """Тестирование получения детальной информации о привычке"""
        response = self.client.get(f"/habits/{self.habit.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_habit(self):
        """Тестирование удаления привычки"""

        response = self.client.delete(f"/habits/{self.habit.pk}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
