from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Post

User = get_user_model()


class PostsURLTests(TestCase):

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
        cls.post = Post.objects.create(
            title='Пост для теста - заголовок1',
            body='Текст тестового поста1',
            user=cls.user_one
        )
        cls.post2 = Post.objects.create(
            title='Пост для теста - заголовок2',
            body='Текст тестового поста2',
            user=cls.user_one
        )
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.author_client = Client()
        cls.author_client.force_login(cls.user_one)
        cls.authorized_client.force_login(cls.user_two)

    def test_urls_are_available_for_guest(self):
        """Проверка доступности страниц из списка
        неавторизованному пользователю."""
        urls_for_guest = [
            ('/', 200),
            (f'/users/{self.user_one.id}/posts/', 200),
            (f'/posts/{self.post.id}/delete/', 302),
            ('/posts/new/', 302),
            ('/404/', 404),
            ('/403/', 403),
            ('/500/', 500),
        ]
        for each_url, code in urls_for_guest:
            with self.subTest(each_url=each_url):
                response = self.guest_client.get(each_url)
                self.assertEqual(response.status_code, code,
                                 f'проверьте {each_url}')

    def test_urls_for_authorized_are_available(self):
        """Проверка доступности страниц из
        списка авторизованному пользователю."""

        urls_for_authorized = [
            (f'/posts/{self.post.id}/delete/', 302),
            ('/posts/new/', 200),
        ]
        for each_url, code in urls_for_authorized:
            with self.subTest(each_url=each_url):
                response = self.authorized_client.get(each_url)
                self.assertEqual(response.status_code, code,
                                 f'проверьте {each_url}')

    def test_urls_for_author_are_available(self):
        """Проверка доступности страниц из списка автору."""

        post_for_del = Post.objects.create(
            title='Пост для удаления - заголовок',
            body='Текст тестового поста для удаления',
            user=self.user_one
        )
        url = f'/posts/{post_for_del.id}/delete/'
        method_code = [
            ('get', 200),
            ('post', 302),
        ]
        for method, code in method_code:
            with self.subTest(method=method):
                client_func = getattr(self.author_client, method)
                response = client_func(url)
                self.assertEqual(response.status_code, code,
                                 f'проверьте {method}')

    def test_urls_use_correct_template_for_guest(self):
        """Проверка на правильность используемого шаблона
        для страниц из словаря, когда к ним обращается
        неавторизованный пользователь."""
        templates_url_names = [
            ('/', 'posts/index.html'),
            (f'/users/{self.user_one.id}/posts/', 'posts/posts.html'),
            ('/404/', 'posts/misc/404.html'),
            ('/403/', 'posts/misc/403.html'),
            ('/500/', 'posts/misc/500.html'),
        ]
        for address, template in templates_url_names:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_use_correct_template_for_authorized(self):
        """Проверка на правильность используемого шаблона
        для страниц из словаря, когда к ним обращается
        авторизованный пользователь."""
        templates_url_names = [
            ('/posts/new/', 'posts/new.html'),
        ]
        for address, template in templates_url_names:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_use_correct_template_for_author(self):
        """Проверка на правильность используемого шаблона
        для страниц из словаря, когда к ним обращается
        автор."""
        templates_url_names = [
            (f'/posts/{self.post.id}/delete/',
             'posts/post_delete.html'),
        ]
        for address, template in templates_url_names:
            with self.subTest(address=address):
                response = self.author_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_redirect_guest_correctly(self):
        """Проверяем для страниц из словаря, что неавторизованный
        пользователь переадресуется на нужную страницу."""
        url_redirects = [
            ('/posts/new/', '/auth/login/?next=/posts/new/'),
            (f'/posts/{self.post.id}/delete/',
             f'/auth/login/?next=/posts/{self.post.id}/delete/'),
        ]
        for address, redir in url_redirects:
            with self.subTest(address=address):
                response = self.guest_client.get(address, follow=True)
                self.assertRedirects(response, redir)

    def test_urls_redirect_athorized_correctly(self):
        """Проверяем что авторизованный пользователь
        переадресуется на нужную страницу."""
        url_redirects = [
            (f'/posts/{self.post.id}/delete/', '/403/'),
        ]
        for address, redir in url_redirects:
            with self.subTest(address=address):
                response = self.authorized_client.get(address, follow=True)
                self.assertRedirects(
                    response,
                    redir,
                    status_code=302,
                    target_status_code=403,
                )

    def test_urls_redirect_author_correctly(self):
        """Проверяем что автор переадресуется на нужную страницу."""
        post_for_del = Post.objects.create(
            title='Пост для удаления - заголовок',
            body='Текст тестового поста для удаления',
            user=self.user_one
        )
        url = f'/posts/{post_for_del.id}/delete/'
        response = self.author_client.post(url, follow=True)
        self.assertRedirects(response, f'/users/{self.user_one.id}/posts/')
