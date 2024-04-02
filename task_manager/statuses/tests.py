from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import Users
from .models import Statuses
from django.utils.translation import gettext as _
from task_manager.settings import FIXTURE_PATH
from task_manager.parser import get_fixture_data
import os
from http import HTTPStatus


class StatusTest(TestCase):
    """Status Tests."""
    fixtures = ['statuses.json', 'users.json']

    def setUp(self):
        """Preparing data for tests."""
        data = get_fixture_data(os.path.join(FIXTURE_PATH, 'data_dump.json'))
        self.new_status = data.get('statuses').get('new_status')
        self.updated_status = data.get('statuses').get('updated_status')
        self.status = Statuses.objects.all().last()
        self.executor = Users.objects.all().first()
        self.task = data.get('tasks').get('update_task')
        self.new_task = {
            "name": self.task['name'],
            "description": self.task['description'],
            "status": self.status.id,
            "executor": self.executor.id,
            "author": self.executor.id
        }

    def test_list_statuses(self):
        """Test statuses index reading."""
        response = self.client.get(reverse('index_statuses'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('index_statuses'))
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_create_status(self):
        """Status creation test."""
        response = self.client.get(reverse('create_status'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('create_status'))
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        self.assertEqual(Statuses.objects.all().count(), 3)

        response_redirect = self.client.post(
            reverse('create_status'),
            data=self.new_status,
            follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_statuses'),
            HTTPStatus.FOUND.value, HTTPStatus.OK.value
        )
        self.assertContains(
            response_redirect,
            _('The status has been successfully created')
        )

    def test_update_status(self):
        """Status update test."""
        response = self.client.get(reverse('update_status', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('update_status', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        response_redirect = self.client.post(
            reverse('update_status', kwargs={'pk': 1}),
            data=self.updated_status,
            follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_statuses'),
            HTTPStatus.FOUND.value, HTTPStatus.OK.value
        )
        self.assertContains(
            response_redirect,
            _('The status has been successfully changed')
        )

    def test_delete_status(self):
        """Status delete test."""
        response = self.client.get(reverse('delete_status', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('delete_status', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

        response_redirect = self.client.post(
            reverse('delete_status', kwargs={'pk': 2}), follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_statuses'),
            HTTPStatus.FOUND.value, HTTPStatus.OK.value
        )
        self.assertContains(
            response_redirect,
            _('The status has been successfully deleted')
        )

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

        response_redirect = self.client.post(
            reverse('delete_status', kwargs={'pk': self.status.id}),
            follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_statuses'),
            HTTPStatus.FOUND.value, HTTPStatus.OK.value
        )
        self.assertContains(
            response_redirect,
            _('It is not possible to delete the status because it is in use')
        )
