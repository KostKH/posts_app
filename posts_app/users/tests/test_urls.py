from django.contrib.auth import get_user_model
from django.test import Client, TestCase

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

        cls.guest_client = Client()

    def test_urls_are_available_for_guest(self):
        """Проверка доступности страниц из списка
        неавторизованному пользователю."""
        urls_for_guest = [
            ('/auth/signup/', 200),
            ('/auth/logout/', 200),
            ('/auth/login/', 200),
        ]
        for each_url, code in urls_for_guest:
            with self.subTest(each_url=each_url):
                response = self.guest_client.get(each_url)
                self.assertEqual(response.status_code, code,
                                 f'проверьте {each_url}')

    def test_urls_use_correct_template_for_guest(self):
        """Проверка на правильность используемого шаблона
        для страниц из словаря, когда к ним обращается
        неавторизованный пользователь."""
        templates_url_names = [
            ('/auth/signup/', 'users/signup.html'),
            ('/auth/logout/', 'users/logged_out.html'),
            ('/auth/login/', 'users/login.html'),
        ]
        for address, template in templates_url_names:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
