from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UsersViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_one = User.objects.create_user(
            name='UserOne',
            email='user_one@test.test',
        )
        cls.guest_client = Client()

    def test_url_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = [
            ('users/login.html', reverse('login')),
            ('users/signup.html', reverse('signup')),
            ('users/logged_out.html', reverse('logout')),
        ]
        for template, reverse_name in templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                cache.clear()
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
