from django.test import TestCase
from apps.category.models import Category
from apps.user.models import User
from apps.category.success_messages import (
    NEW_CATEGORY_CREATED_MESSAGE,
    CATEGORY_UPDATED_SUCCESSFULLY_MESSAGE,
    CATEGORY_WAS_DELETED_SUCCESSFUL
)
from rest_framework.test import APIClient
from rest_framework import status


class CategoryListGenericViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test.email@mail.ru',
            first_name='test',
            last_name='user',
            username='testUser',
            password='password'
        )
        self.client = APIClient()
        self.category = Category.objects.create(name="Test Category")

    def test_get_category_list_unauthenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('http://127.0.0.1:8000/api/v1/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.category.name)
        self.assertIsInstance(response.data, list)
        for category in response.data:
            self.assertIsInstance(category['name'], str)

    def test_get_category_list_empty(self):
        self.client.force_authenticate(user=self.user)
        Category.objects.all().delete()
        response = self.client.get('http://127.0.0.1:8000/api/v1/categories/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, [])

    def test_create_category_unauthenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Test Category 2'}
        response = self.client.post('http://127.0.0.1:8000/api/v1/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], NEW_CATEGORY_CREATED_MESSAGE)
        self.assertEqual(len(response.data), 2)


class RetrieveCategoryGenericViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test.email@mail.ru',
            first_name='test',
            last_name='user',
            username='testUser',
            password='password'
        )
        self.client = APIClient()
        self.category = Category.objects.create(name="Test Category")

    def test_get_category_list_unauthenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'http://127.0.0.1:8000/api/v1/categories/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)

    def test_update_category(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Updated Category'}
        response = self.client.put(f'http://127.0.0.1:8000/api/v1/categories/{self.category.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], CATEGORY_UPDATED_SUCCESSFULLY_MESSAGE)
        self.assertEqual(Category.objects.get(id=self.category.id).name, 'Updated Category')

    def test_delete_category(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'http://127.0.0.1:8000/api/v1/categories/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CATEGORY_WAS_DELETED_SUCCESSFUL)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())
