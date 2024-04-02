from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import Users
from .models import Labels
from task_manager.statuses.models import Statuses
from django.utils.translation import gettext as _
from task_manager.settings import FIXTURE_PATH
from task_manager.parser import get_fixture_data
import os
from http import HTTPStatus


class LabelTest(TestCase):
    """Label Tests."""
    fixtures = ['labels.json', 'users.json', 'statuses.json']

    def setUp(self):
        """Preparing data for tests."""
        data = get_fixture_data(os.path.join(FIXTURE_PATH, 'data_dump.json'))
        self.new_label = data.get('labels').get('new_label')
        self.updated_label = data.get('labels').get('updated_label')
        self.status = Statuses.objects.all().last()
        self.executor = Users.objects.all().first()
        self.label = Labels.objects.all().first()
        self.task = data.get('tasks').get('update_task')
        self.new_task = {
            "name": self.task['name'],
            "description": self.task['description'],
            "status": self.status.id,
            "executor": self.executor.id,
            "author": self.executor.id,
            "labels": self.label.id
        }

    def test_list_labels(self):
        """Test labels index reading."""
        response = self.client.get(reverse('index_labels'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('index_labels'))
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_create_label(self):
        """Label creation test."""
        response = self.client.get(reverse('create_label'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('create_label'))
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        self.assertEqual(Labels.objects.all().count(), 3)

        response_redirect = self.client.post(
            reverse('create_label'),
            data=self.new_label,
            follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_labels'),
            HTTPStatus.FOUND.value, HTTPStatus.OK.value
        )
        self.assertContains(
            response_redirect,
            _('The label was created successfully')
        )

    def test_update_label(self):
        """Label update test."""
        response = self.client.get(reverse('update_label', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('update_label', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        response_redirect = self.client.post(
            reverse('update_label', kwargs={'pk': 1}),
            data=self.updated_label,
            follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_labels'),
            HTTPStatus.FOUND.value, HTTPStatus.OK.value
        )
        self.assertContains(
            response_redirect,
            _('The label has been successfully changed')
        )

    def test_delete_label(self):
        """Label delete test."""
        response = self.client.get(reverse('delete_label', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('delete_label', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

        response_redirect = self.client.post(
            reverse('delete_label', kwargs={'pk': 2}), follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_labels'),
            HTTPStatus.FOUND.value, HTTPStatus.OK.value
        )
        self.assertContains(
            response_redirect,
            _('The label was successfully deleted')
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

        # response_redirect = self.client.post(
        #     reverse('delete_label', kwargs={'pk': self.label.id}),
        #     follow=True
        # )
        # self.assertRedirects(
        #     response_redirect, reverse('index_labels'),
        #     HTTPStatus.FOUND.value, HTTPStatus.OK.value
        # )
        # self.assertContains(
        #     response_redirect,
        #     _('It is not possible to delete a label because it is being used')
        # )
