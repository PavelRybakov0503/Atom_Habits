from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """ Тестов вьюшек """

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='Test',
            password='Test',
            telegram_username='Test',
            telegram_chat_id='Test'
        )

        self.habit = Habit.objects.create(
            owner=self.user,
            place="Test",
            time='15:00',
            action="Test",
            periodicity=1,
            time_to_complete=5,
            pleasant_habit=False,
            is_public=False
        )

    def test_get_habit(self):
        """ Тест HabitListAPIView для получения всех привычек пользователя """

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            reverse('app_habits:habit_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            Habit.objects.all().count(),
            1
        )

    def test_get_habit_public(self):
        """ Тест PublicHabitListAPIView для получения публичных привычек """

        response = self.client.get(
            reverse('app_habits:habit_public_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            Habit.objects.filter(is_public=True).count(),
            0
        )

    def test_post_habit(self):
        """ Тест HabitCreateAPIView для создания привычки """

        self.client.force_authenticate(
            user=self.user
        )

        data = {
            'place': "Test create",
            'time': '15:00',
            'action': "Test create",
            'periodicity': 1,
            'time_to_complete': 10,
            'pleasant_habit': False,
            'is_public': True,
        }

        response = self.client.post(
            reverse('app_habits:habit_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Habit.objects.all().count(),
            2
        )

    def test_lesson_retrieve(self):
        """ Тест HabitRetrieveAPIView для просмотра привычки """

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.get(
            reverse('app_habits:habit_detail',
                    args=[self.habit.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_patch_habit(self):
        """ Тест HabitUpdateAPIView для редактирования привычки """

        self.client.force_authenticate(
            user=self.user
        )

        data = {
            "place": "Новый тест",
            "action": "Новый тест",
        }

        response = self.client.patch(
            reverse(
                'app_habits:habit_update',
                args=[self.habit.id]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.habit.refresh_from_db()

        self.assertEqual(
            self.habit.action,
            'Новый тест'
        )

    def test_delete_habit(self):
        """ Тест HabitDestroyAPIView удаления привычки """
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.delete(
            reverse(
                'app_habits:habit_delete',
                args=[self.habit.pk]
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Habit.objects.all().count(),
            0
        )


class HabitExceptionTestCase(APITestCase):
    """ Тестов отработки исключений """

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='Test',
            password='Test',
            telegram_username='Test',
            telegram_chat_id='Test'
        )

        self.habit = Habit.objects.create(
            owner=self.user,
            place="Test",
            time='15:00',
            action="Test",
            periodicity=1,
            time_to_complete=5,
            pleasant_habit=False,
            is_public=False
        )

    def test_get_other_owner(self):
        """ Проверки просмотра привычек другим пользователем """

        other_user = User.objects.create(
            username='Other_test',
            password='Other_test',
            telegram_username='Other_test',
            telegram_chat_id='Other_test'
        )
        self.client.force_authenticate(
            user=other_user
        )

        response = self.client.get(
            reverse('app_habits:habit_detail',
                    args=[self.habit.pk]),

        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_post_habit_exception_related_habit(self):
        """ Теста проверки приятной привычки наличия вознаграждения или связанной привычки """

        self.client.force_authenticate(
            user=self.user
        )

        data = {
            "owner": self.user.id,
            "place": "Новый тест",
            "time": '15:00',
            "action": "Новый тест",
            "periodicity": 1,
            "time_to_complete": 10,
            "is_public": True,

            "pleasant_habit": True,
            "reward": "Вознаграждения не должно быть!"
        }

        response = self.client.post(
            reverse('app_habits:habit_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(response.json(),
                         {'non_field_errors': ['У приятной привычки не должно быть вознаграждения '
                                               'или связанной привычки!']})

    def test_post_habit_exception_reward(self):
        """ Теста проверки у привычки наличия связанной привычки или вознаграждения """

        self.client.force_authenticate(
            user=self.user
        )

        data = {
            "owner": self.user.id,
            "place": "Новый тест",
            "time": '15:00',
            "action": "Новый тест",
            "periodicity": 1,
            "time_to_complete": 10,
            "pleasant_habit": True,
            "is_public": True,

            "related_habit": self.habit.id,
            "reward": "Связанная привычка или вознаграждение!"
        }

        response = self.client.post(
            reverse('app_habits:habit_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(response.json(),
                         {'non_field_errors': ['Привычка должна быть либо со связанной привычкой, '
                                               'либо с награждением!']})

    def test_post_habit_exception_pleasant_habit(self):
        """ Теста проверки наличия у связанной привычки признака приятности """

        self.client.force_authenticate(
            user=self.user
        )

        data = {
            "owner": self.user.id,
            "place": "Новый тест",
            "time": '15:00',
            "action": "Новый тест",
            "periodicity": 1,
            "time_to_complete": 10,
            "pleasant_habit": False,
            "is_public": True,

            "related_habit": self.habit.id,
        }

        response = self.client.post(
            reverse('app_habits:habit_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(response.json(),
                         {'non_field_errors': ['Связанная привычка должна быть приятной!']})

    def test_post_habit_exception_periodicity(self):
        """ Проверки периодичности привычки на выполнение не реже 1 раза в 7 дней """

        self.client.force_authenticate(
            user=self.user
        )

        data = {
            "owner": self.user.id,
            "place": "Новый тест",
            "time": '15:00',
            "action": "Новый тест",
            "periodicity": 12,
            "time_to_complete": 10,
            "pleasant_habit": True,
            "is_public": True,
        }

        response = self.client.post(
            reverse('app_habits:habit_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ["Привычка должна выполняться не реже 1 раза в 7 дней!"]}
        )

    def test_post_habit_exception_time_to_complete(self):
        """ Проверки выполнения привычки (должно быть не более 120 секунд) """

        self.client.force_authenticate(
            user=self.user
        )

        data = {
            "owner": self.user.id,
            "place": "Новый тест",
            "time": '15:00',
            "action": "Новый тест",
            "periodicity": 3,
            "time_to_complete": 121,
            "pleasant_habit": True,
            "is_public": True,
        }

        response = self.client.post(
            reverse('app_habits:habit_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            ['Время выполнения привычки должно быть больше 0 и меньше 120 секунд!']
        )
