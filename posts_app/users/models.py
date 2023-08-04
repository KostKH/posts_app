from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import CharField, EmailField
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    """Класс для обработки операций с моделью User. Данный класс
    переопределяет методы создания пользователя и суперпользователя:
    были убраны ссылки на username, так как из модели мы это поле
    убрали."""

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Класс User создает БД SQL для хранения
    информации о пользователях."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]
    objects = CustomUserManager()

    username = None
    first_name = None
    last_name = None

    email = EmailField(_('email address'), blank=False, unique=True)
    name = CharField('Имя', max_length=150, blank=False)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
