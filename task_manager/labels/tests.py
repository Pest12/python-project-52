from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import Users
from .models import Labels
from django.utils.translation import gettext as _
from task_manager.settings import FIXTURE_PATH
from task_manager.parser import get_fixture_data
import os


class LabelTest(TestCase):
    fixtures = ['labels.json', 'users.json']

    def setUp(self):
        data = get_fixture_data(os.path.join(FIXTURE_PATH, 'data_dump.json'))
        self.new_label = data.get('labels').get('new_label')
        self.updated_label = data.get('labels').get('updated_label')

    def test_list_labels(self):
        response = self.client.get(reverse('index_labels'))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('index_labels'))
        self.assertEqual(response.status_code, 200)

    def test_create_label(self):
        response = self.client.get(reverse('create_label'))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('create_label'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Labels.objects.all().count(), 3)

        response_redirect = self.client.post(
            reverse('create_label'),
            data=self.new_label,
            follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_labels'), 302, 200
        )
        self.assertContains(
            response_redirect,
            _('The label was created successfully')
        )

    def test_update_label(self):
        response = self.client.get(reverse('update_label', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('update_label', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        response_redirect = self.client.post(
            reverse('update_label', kwargs={'pk': 1}),
            data=self.updated_label,
            follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_labels'), 302, 200
        )
        self.assertContains(
            response_redirect,
            _('The label has been successfully changed')
        )

    def test_delete_label(self):
        response = self.client.get(reverse('delete_label', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('delete_label', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)

        response_redirect = self.client.post(
            reverse('delete_label', kwargs={'pk': 2}), follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_labels'), 302, 200
        )
        self.assertContains(
            response_redirect,
            _('The label was successfully deleted')
        )
