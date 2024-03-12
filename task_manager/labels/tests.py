from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Labels


class CRUD_Labels_Test(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user1 = user_model.objects.create_user(
            first_name='Konstantin',
            last_name='Lugovskikh',
            username='Kostya11',
            password='Kostya'
        )
        Labels.objects.create(name='Label1')
        Labels.objects.create(name='Label2')

    def test_IndexLabels(self):
        self.client.login(username='Kostya11', password='Kostya')
        response = self.client.get(reverse('index_labels'))
        self.assertEqual(response.status_code, 200)

    def test_CreateLabel(self):
        response = self.client.get(reverse('create_label'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='Kostya11', password='Kostya')
        response = self.client.get(reverse('create_label'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/create.html')

        response = self.client.post(
            reverse('create_label'),
            {
                'name': 'new label',
            }
        )
        self.assertRedirects(response, reverse('index_labels'), 302, 200)

    def test_UpdateLabel(self):
        label = Labels.objects.get(id=1)
        response = self.client.get(f'/labels/{label.id}/update/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='Kostya11', password='Kostya')
        response = self.client.get(f'/labels/{label.id}/update/')
        self.assertEqual(response.status_code, 200)
        response_redirect = self.client.post(
            f'/labels/{label.id}/update/',
            {
                'name': 'updated label',
            }
        )
        self.assertRedirects(
            response_redirect, reverse('index_labels'), 302, 200
        )

    def test_DeleteLabel(self):
        label = Labels.objects.get(id=2)
        response = self.client.get(f'/labels/{label.id}/delete/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='Kostya11', password='Kostya')
        response = self.client.get(f'/labels/{label.id}/delete/')
        self.assertEqual(response.status_code, 200)

        response_redirect = self.client.post(f'/labels/{label.id}/delete/')
        self.assertRedirects(
            response_redirect, reverse('index_labels'), 302, 200
        )
