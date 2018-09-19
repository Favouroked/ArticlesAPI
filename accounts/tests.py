from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
User = get_user_model()


class AccountsTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(email='test@test.com', name='test doe', bio='test bio')
        test_user.set_password('testpassword')
        test_user.save()

    def test_create_account(self):
        url = reverse('signup')
        data = {'name': "John Doe", "email": "johndoe@test.com", "password": "awesome", "bio": "Test Doe"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().name, 'John Doe')

    def test_login_account(self):
        url = reverse('signin')
        data = {'email': "test@test.com", 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIsNotNone(response.data.get('token'))
