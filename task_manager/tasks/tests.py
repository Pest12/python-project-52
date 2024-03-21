from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels
from .models import Tasks


class TaskTest(TestCase):
    fixtures = ['tasks.json', 'users.json', 'statuses.json', 'labels.json']

    def test_list_tasks(self):
        response = self.client.get(reverse('index_tasks'))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('index_tasks'))
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        status = Statuses.objects.all().first()
        label = Labels.objects.all().first()
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('create_task'),
            {
                'name': 'new task',
                'descrpition': 'this is new task',
                'author': user.id,
                'status': status.id,
                'executor': user.id,
                'label': label.id
            }
        )
        self.assertRedirects(response, reverse('index_tasks'), 302, 200)

    def test_update_task(self):
        response = self.client.get(reverse('update_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('update_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        status = Statuses.objects.all().first()
        response_redirect = self.client.post(
            reverse('update_task', kwargs={'pk': 1}),
            {
                'name': 'changed task',
                'descrpition': 'this is changed task',
                'author': user.id,
                'status': status.id,
                'executor': user.id,
            }
        )
        self.assertRedirects(
            response_redirect, reverse('index_tasks'), 302, 200
        )

    def test_delete_task(self):
        response = self.client.get(reverse('delete_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('delete_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

        response_redirect = self.client.post(
            reverse('delete_task', kwargs={'pk': 2})
        )
        self.assertRedirects(
            response_redirect, reverse('index_tasks'), 302, 200
        )
        self.assertEqual(Tasks.objects.all().count(), 3)
