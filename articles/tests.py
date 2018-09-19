from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from articles.models import Article

# Create your tests here.
User = get_user_model()


class ArticlesTest(APITestCase):
    token = []

    @classmethod
    def setUpTestData(cls):
        cli = APIClient()
        test_user = User.objects.create(email='test@test.com', name='test doe', bio='test bio')
        test_user.set_password('testpassword')
        test_user.save()
        login_url = reverse('signin')
        login_data = {'email': 'test@test.com', 'password': 'testpassword'}
        response = cli.post(login_url, login_data, format='json')
        tok = response.data.get('token')
        cls.token.append(tok.decode('utf-8'))
        url = reverse('submit_article')
        cli.credentials(HTTP_AUTHORIZATION='Bearer ' + tok.decode('utf-8'))
        data = {'title': 'a title', 'content': 'a content'}
        response = cli.post(url, data, format='json')

    def test_create_article(self):
        url = reverse('submit_article')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token[0])
        data = {'title': 'a title', 'content': 'a content'}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)

    def test_edit_article(self):
        url = reverse('edit_article')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token[0])
        data = {'title': 'modified', 'content': 'a content', 'id': 1}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.first().title, 'modified')

    def test_delete_article(self):
        url = reverse('delete_article')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token[0])
        data = {'id': 1}
        response = client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.count(), 0)

    def test_all_articles(self):
        url = reverse('all_articles')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token[0])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.count(), len(response.data))

    def test_articles_by_individual_writers(self):
        url = reverse('individual_writer', kwargs={'writer_id': 1})
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token[0])
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.filter(user_id=1).count(), len(response.data))
