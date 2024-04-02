from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from django.utils.translation import gettext as _
from task_manager.settings import FIXTURE_PATH
from task_manager.parser import get_fixture_data
import os
from http import HTTPStatus


class TaskTest(TestCase):
    """Task Tests."""
    fixtures = ['tasks.json', 'users.json', 'statuses.json', 'labels.json']

    def setUp(self):
        """Preparing data for tests."""
        data = get_fixture_data(
            os.path.join(FIXTURE_PATH, 'data_dump.json')
        ).get('tasks')
        self.new_task = data.get('new_task')
        self.status = Statuses.objects.all().first()
        self.executor = Users.objects.all().first()
        update_name = data.get('update_task').get('name')
        update_description = data.get('update_task').get('description')
        self.updated_task = {
            "name": update_name,
            "description": update_description,
            "status": self.status.id,
            "executor": self.executor.id,
        }

    def test_list_tasks(self):
        """Test tasks index reading."""
        response = self.client.get(reverse('index_tasks'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('index_tasks'))
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_create_task(self):
        """Task creation test."""
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

        response_redirect = self.client.post(
            reverse('create_task'),
            data=self.new_task,
            follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_tasks'),
            HTTPStatus.FOUND.value, HTTPStatus.OK.value
        )
        self.assertContains(
            response_redirect,
            _('The task has been successfully created')
        )

    def test_update_task(self):
        """Task update test."""
        response = self.client.get(reverse('update_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('update_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        response_redirect = self.client.post(
            reverse('update_task', kwargs={'pk': 1}),
            data=self.updated_task,
            follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_tasks'),
            HTTPStatus.FOUND.value, HTTPStatus.OK.value
        )
        self.assertContains(
            response_redirect,
            _('The task has been successfully changed')
        )

    def test_delete_task(self):
        """Task delete test."""
        response = self.client.get(reverse('delete_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('delete_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

        response_redirect = self.client.post(
            reverse('delete_task', kwargs={'pk': 1}), follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_tasks'),
            HTTPStatus.FOUND.value, HTTPStatus.OK.value
        )
        self.assertContains(
            response_redirect,
            _('The task was successfully deleted')
        )

        response_redirect = self.client.post(
            reverse('delete_task', kwargs={'pk': 2}), follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_tasks'),
            HTTPStatus.FOUND.value, HTTPStatus.OK.value
        )
        self.assertContains(
            response_redirect,
            _('Only the author of the task can delete it.')
        )
