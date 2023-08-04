from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Post

User = get_user_model()


class PostsModelsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_one = User.objects.create_user(
            name='UserOne',
            email='user_one@test.test',
        )
        cls.post = Post.objects.create(
            title='Пост для теста - заголовок1',
            body='Текст тестового поста1',
            user=cls.user_one
        )

    def test_verbose_name(self):
        """Проверяем, что verbose_name в полях совпадает с ожидаемым."""
        field_verboses = [
            (self.post, 'title', 'Заголовок поста'),
            (self.post, 'body', 'Текст поста'),
            (self.post, 'user', 'Автор поста'),
        ]
        for item, field, expected_value in field_verboses:
            with self.subTest(field=field):
                self.assertEqual(
                    item._meta.get_field(field).verbose_name,
                    expected_value
                )
