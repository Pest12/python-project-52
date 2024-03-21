from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import Users
from .models import Labels


class LabelTest(TestCase):
    fixtures = ['labels.json', 'users.json']

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

        response = self.client.post(
            reverse('create_label'),
            {
                'name': 'new label',
            }
        )
        self.assertRedirects(response, reverse('index_labels'), 302, 200)

    def test_update_label(self):
        response = self.client.get(reverse('update_label', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('update_label', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        response_redirect = self.client.post(
            reverse('update_label', kwargs={'pk': 1}),
            {
                'name': 'updated label',
            }
        )
        self.assertRedirects(
            response_redirect, reverse('index_labels'), 302, 200
        )

    def test_delete_label(self):
        response = self.client.get(reverse('delete_label', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('delete_label', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)

        response_redirect = self.client.post(
            reverse('delete_label', kwargs={'pk': 2})
        )
        self.assertRedirects(
            response_redirect, reverse('index_labels'), 302, 200
        )
