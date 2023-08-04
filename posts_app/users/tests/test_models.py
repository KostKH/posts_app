from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UsersModelsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(
            name='UserOne',
            email='user_one@test.test',
        )

    def test_verbose_name(self):
        """Проверяем, что verbose_name в полях совпадает с ожидаемым."""
        field_verboses = [
            (self.user, 'name', 'Имя'),
            (self.user, 'email', _('email address')),
        ]
        for item, field, expected_value in field_verboses:
            with self.subTest(field=field):
                self.assertEqual(
                    item._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_user_str_method_returns_email(self):
        """Проверяем, что метод str возвращает email."""
        self.assertEqual(str(self.user), self.user.email)
