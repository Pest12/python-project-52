from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import Users
from .models import Statuses
from django.utils.translation import gettext as _
from task_manager.settings import FIXTURE_PATH
from task_manager.parser import get_fixture_data
import os


class StatusTest(TestCase):
    fixtures = ['statuses.json', 'users.json']

    def setUp(self):
        data = get_fixture_data(os.path.join(FIXTURE_PATH, 'data_dump.json'))
        self.new_status = data.get('statuses').get('new_status')
        self.updated_status = data.get('statuses').get('updated_status')

    def test_list_statuses(self):
        response = self.client.get(reverse('index_statuses'))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('index_statuses'))
        self.assertEqual(response.status_code, 200)

    def test_create_status(self):
        response = self.client.get(reverse('create_status'))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('create_status'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Statuses.objects.all().count(), 3)

        response_redirect = self.client.post(
            reverse('create_status'),
            data=self.new_status,
            follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_statuses'), 302, 200
        )
        self.assertContains(
            response_redirect,
            _('The status has been successfully created')
        )

    def test_update_status(self):
        response = self.client.get(reverse('update_status', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('update_status', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        response_redirect = self.client.post(
            reverse('update_status', kwargs={'pk': 1}),
            data=self.updated_status,
            follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_statuses'), 302, 200
        )
        self.assertContains(
            response_redirect,
            _('The status has been successfully changed')
        )

    def test_delete_status(self):
        response = self.client.get(reverse('delete_status', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('delete_status', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)

        response_redirect = self.client.post(
            reverse('delete_status', kwargs={'pk': 2}), follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_statuses'), 302, 200
        )
        self.assertContains(
            response_redirect,
            _('The status has been successfully deleted')
        )
