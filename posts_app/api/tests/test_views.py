from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
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

    def test_api_user_list_get_returns_correct_data(self):
        """Метод GET Эндпойнта api-user-list отдает правильный ответ."""
        response = self.guest_client.get(reverse('api-user-list'))
        expected_users = User.objects.all().order_by('-id')
        expected_keys = sorted(['id', 'name', 'email'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(expected_users))
        for user_idx, response_user in enumerate(response.data):
            self.assertEqual(sorted(response_user.keys()), expected_keys)
            for key, response_value in response_user.items():
                expected_value = getattr(expected_users[user_idx], key)
                self.assertEqual(response_value, expected_value)

    def test_api_user_list_invalid_methods_not_allowed(self):
        """Эндпойнт api-user-list не принимает запросы
        с неразрешенными методами."""
        methods = ['POST', 'PUT', 'PATCH', 'DELETE']
        for method in methods:
            with self.subTest(method=method):
                request_method = getattr(self.guest_client, method.lower())
                response = request_method(reverse('api-user-list'))
                self.assertEqual(
                    response.status_code,
                    status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_signup_post_returns_correct_data(self):
        """Метод POST Эндпойнта api-signup отдает правильный ответ."""
        user_data = {
            'name': 'UserTest1',
            'email': 'user_test1@test.test',
            'password': 'PassPass123.'
        }
        response = self.guest_client.post(
            reverse('api-signup'),
            data=user_data,
            format='json'
        )
        expected_user = User.objects.all().order_by('-id').first()
        expected_keys = sorted(['id', 'name', 'email'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(sorted(response.data.keys()), expected_keys)
        for key, response_value in response.data.items():
            expected_value = getattr(expected_user, key)
            self.assertEqual(response_value, expected_value)

    def test_api_signup_post_invalid_data_fails(self):
        """Метод POST Эндпойнта api-signup при отправке некорректных данных
        не создает пользователя и возвращает код 400."""
        len_users_before = len(User.objects.all())
        user_data = {
            'name': 'UserTest2',
            'email': 'user_test2@test.test',
            'password': 'PassPass123.'
        }
        for key in user_data.keys():
            with self.subTest(key=key):
                invalid_data = user_data.copy()
                invalid_data.pop(key)
                response = self.guest_client.post(
                    reverse('api-signup'),
                    data=invalid_data,
                    format='json')
                len_users_after = len(User.objects.all())
                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST)
                self.assertEqual(len_users_before, len_users_after)

    def test_api_signup_invalid_methods_not_allowed(self):
        """Эндпойнт api-signup не принимает запросы
        с неразрешенными методами."""
        methods = ['GET', 'PUT', 'PATCH', 'DELETE']
        len_users_before = len(User.objects.all())

        for method in methods:
            with self.subTest(method=method):
                request_method = getattr(self.guest_client, method.lower())
                response = request_method(reverse('api-signup'))
                len_users_after = len(User.objects.all())
                self.assertEqual(
                    response.status_code,
                    status.HTTP_405_METHOD_NOT_ALLOWED)
                self.assertEqual(len_users_before, len_users_after)

    def test_api_user_posts_invalid_methods_not_allowed(self):
        """Эндпойнт api-user-posts не принимает запросы
        с неразрешенными методами."""
        methods = ['POST', 'PUT', 'PATCH', 'DELETE']

        for method in methods:
            with self.subTest(method=method):
                request_method = getattr(self.guest_client, method.lower())
                response = request_method(
                    reverse('api-user-posts', args=[self.user_one.id]))
                self.assertEqual(
                    response.status_code,
                    status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_user_posts_get_returns_correct_data(self):
        """Метод GET Эндпойнта api-user-posts отдает правильный ответ."""
        response = self.guest_client.get(
            reverse('api-user-posts', args=[self.user_one.id]))
        expected_posts = Post.objects.all().order_by('-id')
        expected_keys = sorted(['id', 'title', 'body', 'user'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(expected_posts))
        for post_idx, response_post in enumerate(response.data):
            self.assertEqual(sorted(response_post.keys()), expected_keys)
            for key, response_value in response_post.items():
                expected_value = getattr(expected_posts[post_idx], key)
                if key == 'user':
                    expected_value = expected_value.id
                self.assertEqual(response_value, expected_value)

    def test_api_login_invalid_methods_not_allowed(self):
        """Эндпойнт api-login не принимает запросы
        с неразрешенными методами."""
        methods = ['GET', 'PUT', 'PATCH', 'DELETE']

        for method in methods:
            with self.subTest(method=method):
                request_method = getattr(self.guest_client, method.lower())
                response = request_method(
                    reverse('api-login'))
                self.assertEqual(
                    response.status_code,
                    status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_login_post_returns_correct_data(self):
        """Метод POST Эндпойнта api-login отдает правильный ответ."""

        user_data = {
            'name': 'UserTestLogin1',
            'email': 'user_test_login1@test.test',
            'password': 'PassPass123.'
        }
        self.guest_client.post(
            reverse('api-signup'),
            data=user_data,
            format='json'
        )
        user_id = User.objects.all().order_by('-id').first().id
        user_data.pop('name')
        response = self.guest_client.post(
            reverse('api-login'),
            data=user_data,
            format='json'
        )
        expected_token = Token.objects.filter(user_id=user_id).first().key
        expected_keys = ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(sorted(response.data.keys()), expected_keys)
        self.assertEqual(response.data.get('token'), expected_token)

    def test_api_login_post_invalid_data_fails(self):
        """Метод POST Эндпойнта api-signup при отправке некорректных данных
        не создает токен и возвращает код 400."""
        user_data = {
            'name': 'UserTestLogin2',
            'email': 'user_test_login1@test.test',
            'password': 'PassPass123.'
        }
        self.guest_client.post(
            reverse('api-signup'),
            data=user_data,
            format='json'
        )
        user_data.pop('name')
        len_tokens_before = len(Token.objects.all())

        for key in user_data.keys():
            invalid_data = user_data.copy()
            invalid_data.pop(key)
            with self.subTest(key=key):
                response = self.guest_client.post(
                    reverse('api-login'),
                    data=invalid_data,
                    format='json')
                self.assertEqual(response.status_code,
                                 status.HTTP_400_BAD_REQUEST)
                len_tokens_after = len(Token.objects.all())
                self.assertEqual(len_tokens_before, len_tokens_after)

    def test_api_post_list_post_returns_correct_data(self):
        """Метод POST Эндпойнта api-post-list отдает правильный ответ."""

        post_data = {
            'title': 'Новый тестовый пост1',
            'body': 'Новый пост1',
        }
        response = self.authorized_client.post(
            reverse('api-post-list'),
            data=post_data,
            format='json'
        )
        expected_post = Post.objects.filter(
            title=post_data['title'],
            body=post_data['body'],
        ).order_by('-id').first()
        expected_keys = sorted(['id', 'title', 'body', 'user'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(sorted(response.data.keys()), expected_keys)
        for key in response.data.keys():
            expected_value = getattr(expected_post, key)
            if key == 'user':
                expected_value = expected_value.id
            self.assertEqual(response.data.get(key), expected_value)

    def test_api_post_list_post_unauthorized_fails(self):
        """неавторизованный пользователь не может создать отправить
           POST-запрос на эндпойнт api-post-list."""
        len_posts_before = len(Post.objects.all())
        post_data = {
            'title': 'Новый тестовый пост2',
            'body': 'Новый пост2',
        }
        response = self.guest_client.post(
            reverse('api-post-list'),
            data=post_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        len_posts_after = len(Post.objects.all())
        self.assertEqual(len_posts_before, len_posts_after)

    def test_api_post_list_post_invalid_data_fails(self):
        """Метод POST Эндпойнта api-post-list при отправке некорректных данных
        не создает пост и возвращает код 400."""
        len_posts_before = len(Post.objects.all())
        post_data = {
            'title': 'Новый тестовый пост3',
            'body': 'Новый пост3',
        }
        for key in post_data.keys():
            with self.subTest(key=key):
                invalid_data = post_data.copy()
                invalid_data.pop(key)
                response = self.authorized_client.post(
                    reverse('api-post-list'),
                    data=invalid_data,
                    format='json')
                len_posts_after = len(Post.objects.all())
                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST)
                self.assertEqual(len_posts_before, len_posts_after)

    def test_api_post_list_invalid_methods_not_allowed(self):
        """Эндпойнт api_post_list не принимает запросы
        с неразрешенными методами."""
        methods = ['GET', 'PUT', 'PATCH', 'DELETE']

        for method in methods:
            with self.subTest(method=method):
                request_method = getattr(
                    self.authorized_client,
                    method.lower())
                response = request_method(
                    reverse('api-post-list'))
                self.assertEqual(
                    response.status_code,
                    status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_post_detail_invalid_methods_not_allowed(self):
        """Эндпойнт api_post_detail не принимает запросы
        с неразрешенными методами."""
        methods = ['GET', 'PUT', 'PATCH', 'POST']

        for method in methods:
            with self.subTest(method=method):
                request_method = getattr(
                    self.author_client,
                    method.lower())
                response = request_method(
                    reverse('api-post-detail', args=[self.post[-1].id]))
                self.assertEqual(
                    response.status_code,
                    status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_post_detail_delete_non_author_fails(self):
        """Не-автор не может удалить пост запросом на api-post-detail."""
        len_posts_before = len(Post.objects.all())
        response = self.authorized_client.delete(
            reverse('api-post-detail', args=[self.post[-1].id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        len_posts_after = len(Post.objects.all())
        self.assertEqual(len_posts_before, len_posts_after)

    def test_api_post_detail_delete_returns_correct_data(self):
        """Метод DELETE эндпойнта api-post-detail отдает правильный ответ."""
        len_posts_before = len(Post.objects.all())
        post_delete_id = Post.objects.filter(user=self.user_one).first().id
        response = self.author_client.delete(
            reverse('api-post-detail', args=[post_delete_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        len_posts_after = len(Post.objects.all())
        self.assertEqual(len_posts_before - 1, len_posts_after)
        search_for_post = Post.objects.filter(id=post_delete_id)
        self.assertFalse(search_for_post)
