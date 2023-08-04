from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Post

User = get_user_model()


class PostsFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.post_form = PostForm()

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
        cls.guest_client = Client()
        cls.author_client = Client()
        cls.author_client.force_login(cls.user_one)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user_two)

    def test_create_valid_post(self):
        """Валидная форма создает запись в Post."""
        post_count = Post.objects.count()
        form_data = {
            'title': 'Новый заголовок',
            'body': 'Новый текст',
        }
        response = self.author_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('user_post_view', args=[self.user_one.id])
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        new_post = Post.objects.filter(
            title=form_data['title'],
            body=form_data['body'],
        ).order_by('-id').first()
        self.assertIsNotNone(new_post)
        self.assertEqual(new_post.title, form_data['title'])
        self.assertEqual(new_post.body, form_data['body'])

    def test_invalid_post_is_not_created(self):
        """Форма с некорректными данными не создает запись в Post."""
        post_count = Post.objects.count()
        form_data = {
            'title': 'П' * 61,
            'body': 'Новый текст',
        }
        response = self.author_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), post_count)
        new_post_search = Post.objects.filter(
            title=form_data['title'],
            body=form_data['body'],
        ).order_by('-id')
        self.assertFalse(new_post_search)
        validated_form = response.context.get('form')
        self.assertFalse(validated_form.is_valid())

    def test_guest_cannot_create_post(self):
        """Не-автор не может создать пост."""
        post_count = Post.objects.count()
        redir = reverse('login') + '?next=' + reverse('new_post')
        form_data = {
            'title': 'Новый заголовок - guest',
            'body': 'Новый текст - guest',
        }
        response_guest = self.guest_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response_guest, redir)
        self.assertEqual(Post.objects.count(), post_count)
