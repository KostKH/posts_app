from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm

User = get_user_model()


class SignUp(CreateView):
    """Класс обрабатывает данные из формы регистрации пользователя,
    возвращает страницу с формой для регистрации,
    после регистрации перенаправляет на страницу входа"""

    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = "users/signup.html"
