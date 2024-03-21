from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import Users
from .models import Statuses


class StatusTest(TestCase):
    fixtures = ['statuses.json', 'users.json']

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

        response = self.client.post(
            reverse('create_status'),
            {
                'name': 'new status',
            }
        )
        self.assertRedirects(response, reverse('index_statuses'), 302, 200)

    def test_update_status(self):
        response = self.client.get(reverse('update_status', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('update_status', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        response_redirect = self.client.post(
            reverse('update_status', kwargs={'pk': 1}),
            {
                'name': 'updated status',
            }
        )
        self.assertRedirects(
            response_redirect, reverse('index_statuses'), 302, 200
        )

    def test_delete_status(self):
        response = self.client.get(reverse('delete_status', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('delete_status', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)

        response_redirect = self.client.post(
            reverse('delete_status', kwargs={'pk': 2})
        )
        self.assertRedirects(
            response_redirect, reverse('index_statuses'), 302, 200
        )
