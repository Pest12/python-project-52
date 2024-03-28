from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import Users
from django.utils.translation import gettext as _
from task_manager.settings import FIXTURE_PATH
from task_manager.parser import get_fixture_data
import os


class UserTest(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        data = get_fixture_data(os.path.join(FIXTURE_PATH, 'data_dump.json'))
        self.new_user = data.get('users').get('new_user')
        self.updated_user = data.get('users').get('updated_user')

    def test_list_users(self):
        response = self.client.get(reverse('index_users'))
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = self.client.get(reverse('create_user'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('create_user'),
            data=self.new_user,
            follow=True
        )
        self.assertRedirects(response, reverse('login'), 302, 200)
        self.assertContains(
            response,
            _('The user has been successfully registered')
        )

    def test_update_user(self):
        response = self.client.get(reverse('update_user', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        another_user = Users.objects.all().last()
        self.client.force_login(user=user)
        response = self.client.get(
            reverse('update_user', kwargs={'pk': user.id})
        )
        self.assertEqual(response.status_code, 200)

        response_redirect = self.client.post(
            reverse('update_user', kwargs={'pk': another_user.id}),
            follow=True
        )
        self.assertContains(
            response_redirect,
            _('You do not have the rights to change another user.')
        )

        response_redirect = self.client.post(
            reverse('update_user', kwargs={'pk': user.id}),
            data=self.updated_user,
            follow=True
        )
        self.assertContains(
            response_redirect,
            _('The user has been successfully changed')
        )
        self.assertRedirects(
            response_redirect, reverse('index_users'), 302, 200
        )

    def test_delete_user(self):
        response = self.client.get(reverse('delete_user', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)

        user = Users.objects.all().first()
        another_user = Users.objects.all().last()
        self.client.force_login(user=user)
        response = self.client.get(
            reverse('delete_user', kwargs={'pk': user.id})
        )
        self.assertEqual(response.status_code, 200)

        response_redirect = self.client.post(
            reverse('delete_user', kwargs={'pk': another_user.id}),
            follow=True
        )
        self.assertContains(
            response_redirect,
            _('You do not have the rights to change another user.')
        )

        response_redirect = self.client.post(
            reverse('delete_user', kwargs={'pk': user.id}),
            follow=True
        )
        self.assertRedirects(
            response_redirect, reverse('index_users'), 302, 200
        )
        self.assertContains(
            response_redirect,
            _('The user has been successfully deleted')
        )
