from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from users.forms import CreationForm

User = get_user_model()


class UsersFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(
            name='UserOne',
            email='user_one@test.test',
        )
        cls.creation_form = CreationForm()
        cls.guest_client = Client()

    def test_create_valid_user(self):
        """Валидная форма создает запись в User."""
        user_count = User.objects.count()
        form_data = {
            'name': 'UserTwo',
            'email': 'user_two@test.test',
            'password1': 'PassPass123.',
            'password2': 'PassPass123.',
        }

        response = self.guest_client.post(
            reverse('signup'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(User.objects.count(), user_count + 1)
        new_user = User.objects.filter(
            email=form_data['email'],
            name=form_data['name'],
        ).order_by('-id').first()
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.email, form_data['email'])
        self.assertEqual(new_user.name, form_data['name'])

    def test_invalid_user_is_not_created(self):
        """Форма с некорректными данными не создает запись в Post."""
        user_count = User.objects.count()
        form_data = {
            'name': 'UserTwo',
            'email': 'user_two@test.test',
            'password1': 'PassPass123.',
            'password2': 'PassPass123.',
        }
        for key in form_data.keys():
            invalid_data = form_data.copy()
            invalid_data.pop(key)
            with self.subTest(key=key):
                response = self.guest_client.post(
                    reverse('signup'),
                    data=invalid_data,
                    follow=True
                )
                self.assertEqual(User.objects.count(), user_count)
                new_user_search = User.objects.filter(
                    email=form_data['email'],
                    name=form_data['name'],
                ).order_by('-id')
                self.assertFalse(new_user_search)
                validated_form = response.context.get('form')
                self.assertFalse(validated_form.is_valid())
