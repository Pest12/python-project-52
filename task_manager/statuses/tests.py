from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Statuses


class CRUD_Status_Test(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user1 = user_model.objects.create_user(
            first_name='Konstantin',
            last_name='Lugovskikh',
            username='Kostya11',
            password='Kostya'
        )
        Statuses.objects.create(name='New')
        Statuses.objects.create(name='Completed')


    def test_status_index(self):
        self.client.login(username='Kostya11', password='Kostya')
        response = self.client.get(reverse('index_statuses'))
        self.assertEqual(response.status_code, 200)


    def test_CreateStatus(self):
        response = self.client.get(reverse('create_status'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='Kostya11', password='Kostya')
        response = self.client.get(reverse('create_status'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/create.html')

        response = self.client.post(
            reverse('create_status'), 
            {
                'name': 'status',
            }
        )
        self.assertRedirects(response, reverse('index_statuses'), 302, 200)


    def test_UpdateStatus(self):
        status = Statuses.objects.get(id=1)
        response = self.client.get(f'/statuses/{status.id}/update/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='Kostya11', password='Kostya')
        response = self.client.get(f'/statuses/{status.id}/update/')
        self.assertEqual(response.status_code, 200)
        response_redirect = self.client.post(
            f'/statuses/{status.id}/update/',
            {
                'name':'updated status',
            }
        )
        self.assertRedirects(response_redirect, reverse('index_statuses'), 302, 200)

    
    def test_DeleteStatus(self):
        status = Statuses.objects.get(id=2)
        response = self.client.get(f'/statuses/{status.id}/delete/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='Kostya11', password='Kostya')
        response = self.client.get(f'/statuses/{status.id}/delete/')
        self.assertEqual(response.status_code, 200)

        response_redirect = self.client.post(f'/statuses/{status.id}/delete/')
        self.assertRedirects(response_redirect, reverse('index_statuses'), 302, 200)

