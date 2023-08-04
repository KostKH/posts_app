from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

from posts.models import Post

User = get_user_model()


class ApiViewsTests(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_one = User.objects.create_user(
            name='UserOne',
            email='user_one@test.test',
        )
        cls.user_two = User.objects.create_user(
            name='UserTwo',
            email='user_two@test.test',
        )
        cls.user_three = User.objects.create_user(
            name='UserThree',
            email='user_three@test.test',
        )
        cls.post = []
        for number in range(3):
            post = Post.objects.create(
                title=f'Пост {number} для теста - заголовок',
                body=f'Тестовый пост {number}.',
                user=cls.user_one,
            )
            cls.post.append(post)

        cls.guest_client = APIClient()
        cls.author_client = APIClient()
        cls.author_client.force_authenticate(user=cls.user_one)
        cls.authorized_client = APIClient()
        cls.authorized_client.force_authenticate(user=cls.user_two)

    def test_urls_are_available_for_guest(self):
        """Проверка доступности страниц из списка
        неавторизованному пользователю."""
        urls_for_guest = [
            ('/api/users/', 200),
            (f'/api/users/{self.user_one.id}/posts/', 200),
        ]
        for each_url, code in urls_for_guest:
            with self.subTest(each_url=each_url):
                response = self.guest_client.get(each_url)
                self.assertEqual(response.status_code, code,
                                 f'проверьте {each_url}')

    def test_urls_for_authorized_are_available(self):
        """Проверка доступности страниц авторизованному пользователю."""
        url_for_authorized = '/api/posts/'
        post_data = {
            'title': 'Новый тестовый пост3',
            'body': 'Новый пост3',
        }
        response = self.authorized_client.post(
            url_for_authorized,
            data=post_data,
            format='json')
        self.assertEqual(response.status_code, 201)

    def test_urls_for_author_are_available(self):
        """Проверка доступности страниц автору."""
        url = f'/api/posts/{self.post[-1].id}/'
        response = self.author_client.delete(url)
        self.assertEqual(response.status_code, 204)
