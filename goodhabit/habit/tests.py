from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Habit

class HabitViewSetTests(TestCase):

    def setUp(self):
        # Создание пользователей
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.staff_user = User.objects.create_user(username='staffuser', password='12345', is_staff=True)

        # Создание публичных и приватных привычек
        self.public_habit = Habit.objects.create(
            user=self.user,
            location='Park',
            time='08:00:00',
            action='Walk',
            is_pleasant=False,
            periodicity=7,
            reward='None',
            time_to_complete=30,
            is_public=True
        )

        self.private_habit = Habit.objects.create(
            user=self.user,
            location='Gym',
            time='07:00:00',
            action='Run',
            is_pleasant=False,
            periodicity=7,
            reward='Reward',
            time_to_complete=60,
            is_public=False
        )

        self.client = APIClient()

    def test_public_habits_list(self):
        response = self.client.get('/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Walk', str(response.content))

    def test_private_habits_not_visible(self):
        response = self.client.get('/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('Run', str(response.content))

    def test_user_cannot_edit_public_habit(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.patch(f'/habits/{self.public_habit.id}/', {'action': 'Updated Action'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete_public_habit(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.delete(f'/habits/{self.public_habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_edit_public_habit(self):
        self.client.login(username='staffuser', password='12345')
        response = self.client.patch(f'/habits/{self.public_habit.id}/', {'action': 'Updated Action'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_can_delete_public_habit(self):
        self.client.login(username='staffuser', password='12345')
        response = self.client.delete(f'/habits/{self.public_habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_habit_belongs_to_current_user(self):
        habit = Habit.objects.create(
            user=self.user,
            location='Home',
            time='10:00:00',
            action='Read',
            is_pleasant=True,
            periodicity=1,
            reward='Coffee',
            time_to_complete=15,
            is_public=False
        )
        self.assertEqual(habit.user, self.user)

    def test_user_cannot_edit_another_private_habit(self):
        other_user = User.objects.create_user(username='otheruser', password='12345')
        private_habit = Habit.objects.create(
            user=other_user,
            location='Cafe',
            time='10:00:00',
            action='Drink Coffee',
            is_pleasant=True,
            periodicity=7,
            reward='Dessert',
            time_to_complete=15,
            is_public=False
        )
        self.client.login(username='testuser', password='12345')
        response = self.client.patch(f'/habits/{private_habit.id}/', {'action': 'Updated Action'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_habit_with_duration_more_than_120_seconds_fails(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/habits/', {
            'user': self.user.id,
            'location': 'Park',
            'time': '06:00:00',
            'action': 'Long Run',
            'is_pleasant': False,
            'periodicity': 7,
            'reward': 'None',
            'time_to_complete': 150,
            'is_public': False
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
