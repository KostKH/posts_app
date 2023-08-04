from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    """Класс генерит форму для создания поста."""

    class Meta:
        model = Post
        fields = [
            'title',
            'body',
        ]
        required = {
            'title': True,
            'body': True,
        }
        help_texts = {
            'title': 'Введите заголовок',
            'body': 'Введите текст поста',
        }
