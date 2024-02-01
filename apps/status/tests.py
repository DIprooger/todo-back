from apps.status.models import Status
from django.test import TestCase
from apps.user.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.status.success_messages import (
    NEW_STATUS_CREATED_MESSAGE,
    STATUS_UPDATED_SUCCESSFULLY_MESSAGE,
    STATUS_WAS_DELETED_SUCCESSFUL
)


class StatusListGenericViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test.email@mail.ru',
            first_name='test',
            last_name='user',
            username='testUser',
            password='password'
        )
        self.client = APIClient()
        self.status1 = Status.objects.create(name="Test Status 1")
        self.status2 = Status.objects.create(name="Test Status 2")

    def test_get_status_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('http://127.0.0.1:8000/api/v1/statuses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn(self.status1.name, [status['name'] for status in response.data])
        self.assertIn(self.status2.name, [status['name'] for status in response.data])

    def test_get_status_list_empty(self):
        self.client.force_authenticate(user=self.user)

        Status.objects.all().delete()
        response = self.client.get('http://127.0.0.1:8000/api/v1/statuses/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, [])

    def test_create_status(self):
        self.client.force_authenticate(user=self.user)

        data = {'name': 'New Status'}
        response = self.client.post('http://127.0.0.1:8000/api/v1/statuses/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], NEW_STATUS_CREATED_MESSAGE)
        self.assertEqual(Status.objects.count(), 3)


class RetrieveStatusGenericViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test.email@mail.ru',
            first_name='test',
            last_name='user',
            username='testUser',
            password='password'
        )
        self.client = APIClient()
        self.status = Status.objects.create(name="Test Status")

    def test_get_status_detail(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f'http://127.0.0.1:8000/api/v1/statuses/{self.status.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.status.name)

    def test_update_status(self):
        self.client.force_authenticate(user=self.user)

        data = {'name': 'Updated Status'}
        response = self.client.put(f'http://127.0.0.1:8000/api/v1/statuses/{self.status.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], STATUS_UPDATED_SUCCESSFULLY_MESSAGE)
        self.assertEqual(Status.objects.get(id=self.status.id).name, 'Updated Status')

    def test_delete_status(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f'http://127.0.0.1:8000/api/v1/statuses/{self.status.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, STATUS_WAS_DELETED_SUCCESSFUL)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

