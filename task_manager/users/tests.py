from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class CRUD_Test(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user1 = user_model.objects.create_user(
            first_name='Konstantin',
            last_name='Lugovskikh',
            username='Kostya11',
            password='Kostya'
        )
        cls.user2 = user_model.objects.create_user(
            first_name='Dmitriy',
            last_name='Buinov',
            username='Dimon',
            password='Dima11'
        )


    def test_user_index(self):
        response = self.client.get(reverse('index_users'))
        self.assertEqual(response.status_code, 200)


    def test_CreateUser(self):
        response = self.client.get(reverse('create_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/create.html')

        response = self.client.post(
            reverse('create_user'), 
            {
                'first_name': 'Kostya',
                'last_name': 'Lugov',
                'username': 'Pest',
                'password1': 'Kostya123',
                'password2': 'kostya123'
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


    def test_UpdateUser(self):
        self.client.login(username='Kostya11', password='Kostya')
        user_id = get_user_model().objects.get(username='Dimon').id
        response = self.client.get(f'/users/{user_id}/update/')
        self.assertRedirects(response, reverse('index_users'), 302, 200)

        user_id = get_user_model().objects.get(username='Kostya11').id
        response = self.client.get(f'/users/{user_id}/update/')
        self.assertEqual(response.status_code, 200)

        response_redirect = self.client.post(
            f'/users/{user_id}/update/',
            {
                'username':'Kostya1212',
                'password1': 'Kostya',
                'password2': 'Kostya'
            }
        )
        self.assertRedirects(response_redirect, reverse('index_users'), 302, 200)

    
    def test_DeleteUser(self):
        self.client.login(username='Kostya11', password='Kostya')
        user_id = get_user_model().objects.get(username='Dimon').id
        response = self.client.get(f'/users/{user_id}/delete/')
        self.assertRedirects(response, reverse('index_users'), 302, 200)

        user_id = get_user_model().objects.get(username='Kostya11').id
        response = self.client.get(f'/users/{user_id}/update/')
        self.assertEqual(response.status_code, 200)

        response_redirect = self.client.post(f'/users/{user_id}/delete/')
        self.assertRedirects(response_redirect, reverse('index_users'), 302, 200)