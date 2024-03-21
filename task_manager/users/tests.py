from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import Users


class UserTest(TestCase):
    fixtures = ['users.json']

    def test_list_users(self):
        response = self.client.get(reverse('index_users'))
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = self.client.get(reverse('create_user'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('create_user'),
            {
                'first_name': 'Kostya',
                'last_name': 'Lugov',
                'username': 'Pest',
                'password1': 'Kostya123',
                'password2': 'kostya1'
            }
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('create_user'),
            {
                'first_name': 'Kostya',
                'last_name': 'Lugov',
                'username': 'Pest',
                'password1': 'Kostya123',
                'password2': 'Kostya123'
            }
        )
        self.assertRedirects(response, reverse('login'), 302, 200)

    def test_update_user(self):
        response = self.client.get(reverse('update_user', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().last()
        self.client.force_login(user=user)
        response = self.client.get(
            reverse('update_user', kwargs={'pk': user.id})
        )
        self.assertEqual(response.status_code, 200)
        response_redirect = self.client.post(
            reverse('update_user', kwargs={'pk': user.id}),
            {
                'username': 'Kostya1212',
                'password1': 'Kostya123',
                'password2': 'Kostya123'
            }
        )
        self.assertRedirects(
            response_redirect, reverse('index_users'), 302, 200
        )

    def test_delete_user(self):
        response = self.client.get(reverse('delete_user', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        self.client.force_login(user=user)
        response = self.client.get(
            reverse('delete_user', kwargs={'pk': user.id})
        )
        self.assertEqual(response.status_code, 200)

        response_redirect = self.client.post(
            reverse('delete_user', kwargs={'pk': user.id})
        )
        self.assertRedirects(
            response_redirect, reverse('index_users'), 302, 200
        )
