from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post

User = get_user_model()


class PostsViewsTests(TestCase):

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
            title='Пост для теста - заголовок',
            body='Текст тестового поста',
            user=cls.user_one
        )

        cls.post = []
        for number in range(20):
            post = Post.objects.create(
                title=f'Пост {number} для теста - заголовок',
                body=f'Тестовый посст {number}.',
                user=cls.user_one,
            )
            cls.post.append(post)

        cls.guest_client = Client()
        cls.author_client = Client()
        cls.author_client.force_login(cls.user_one)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user_two)

    def test_url_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        post = self.post[-1]
        templates_pages_names = [
            ('posts/index.html', reverse('index')),
            ('posts/posts.html',
             reverse('user_post_view', args=[self.user_one.id])),
            ('posts/new.html', reverse('new_post')),
            ('posts/post_delete.html',
             reverse('post_delete', args=[post.id])),
            ('posts/misc/404.html', reverse('err404')),
            ('posts/misc/500.html', reverse('err500')),
            ('posts/misc/403.html', reverse('err403')),
        ]
        for template, reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.author_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_shows_correct_context(self):
        """В шаблон index передан правильный контекст."""
        response = self.guest_client.get(reverse('index'))
        user = response.context.get('page')[0]
        expected_user = self.user_two
        self.assertEqual(user.id, expected_user.id)
        self.assertEqual(user.name, expected_user.name)
        self.assertEqual(user.email, expected_user.email)

    def test_posts_shows_correct_context(self):
        """В шаблон posts передан правильный контекст."""
        expected_post = self.post[-1]
        response = self.author_client.get(
            reverse('user_post_view', args=[self.user_one.id]))
        post = response.context.get('page')[0]
        expected_post = self.post[-1]
        self.assertEqual(post.id, expected_post.id)
        self.assertEqual(post.title, expected_post.title)
        self.assertEqual(post.body, expected_post.body)
        self.assertEqual(post.user, expected_post.user)
        self.assertTrue(response.context.get('is_author'))

    def test_new_shows_correct_context(self):
        """В шаблон new передан правильный контекст."""
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = response.context.get('form').fields
        fields_should_be = {
            'title': forms.CharField,
            'body': forms.CharField,
        }
        for field, expected in fields_should_be.items():
            with self.subTest(field=field):
                self.assertIsInstance(form_fields.get(field), expected)

    def test_post_delete_shows_correct_context(self):
        """В шаблон post_delete передан правильный контекст."""
        expected_post = self.post[0]
        response = self.author_client.get(
            reverse('post_delete', args=[expected_post.id]))
        post = response.context.get('post')
        self.assertEqual(post.id, expected_post.id)
        self.assertEqual(post.title, expected_post.title)
        self.assertEqual(post.body, expected_post.body)
        self.assertEqual(post.user, expected_post.user)
