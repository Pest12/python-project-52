from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Statuses
from .models import Tasks


class CRUD_Tasks_Test(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user1 = user_model.objects.create_user(
            first_name='Konstantin',
            last_name='Lugovskikh',
            username='Kostya11',
            password='Kostya'
        )
        cls.status1 = Statuses.objects.create(name='New')
        cls.status2 = Statuses.objects.create(name='Completed')

        Tasks.objects.create(
            name='task1_name',
            description='description',
            executor=cls.user1,
            status=cls.status1,
            author=cls.user1,
        )
        Tasks.objects.create(
            name='task2_name',
            description='description',
            executor=cls.user1,
            status=cls.status2,
            author=cls.user1,
        )

    def test_task_index(self):
        self.client.login(username='Kostya11', password='Kostya')
        response = self.client.get(reverse('index_tasks'))
        self.assertEqual(response.status_code, 200)

    def test_CreateTask(self):
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='Kostya11', password='Kostya')
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/create.html')

        response = self.client.post(
            reverse('create_task'),
            {
                'name': 'first task',
                'descrpition': 'new task',
                'status': 1,
                'executor': 1,
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_UpdateTask(self):
        task = Tasks.objects.get(id=1)
        response = self.client.get(f'/tasks/{task.id}/update/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='Kostya11', password='Kostya')
        response = self.client.get(f'/tasks/{task.id}/update/')
        self.assertEqual(response.status_code, 200)
        response_redirect = self.client.post(
            f'/tasks/{task.id}/update/',
            {
                'name': 'changed task',
                'descrpition': 'new task',
                'status': 1,
                'executor': 1,
            }
        )
        self.assertEqual(response_redirect.status_code, 200)

    def test_DeleteTask(self):
        task = Tasks.objects.get(id=2)
        response = self.client.get(f'/tasks/{task.id}/delete/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='Kostya11', password='Kostya')
        response = self.client.get(f'/tasks/{task.id}/delete/')
        self.assertEqual(response.status_code, 200)

        response_redirect = self.client.post(f'/tasks/{task.id}/delete/')
        self.assertRedirects(
            response_redirect, reverse('index_tasks'), 302, 200
        )
