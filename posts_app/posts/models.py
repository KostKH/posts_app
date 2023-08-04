from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    """Класс Post создает БД SQL для хранения статей."""

    title = models.CharField(
        verbose_name='Заголовок поста',
        max_length=60
    )
    body = models.TextField(
        verbose_name='Текст поста',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор поста',
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.title[:25]
