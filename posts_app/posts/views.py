from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post

User = get_user_model()


def index(request):
    """Функция возвращает объект класса BaseManager (результат SQL-запроса)
    со статьями из БД Posts и возвращает сгенерированную страницу."""
    user_list = User.objects.all()
    paginator = Paginator(user_list, settings.PAGE_NO)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/index.html', {'page': page})


def user_post_view(request, user_id):
    """Функция возвращает объект класса BaseManager (результат SQL-запроса)
    со статьями из БД Posts и возвращает сгенерированную страницу."""
    user = get_object_or_404(User, id=user_id)
    post_list = user.posts.all()
    is_author = bool(request.user == user)
    paginator = Paginator(post_list, settings.PAGE_NO)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'posts/posts.html',
        {'page': page, 'name': user.name, 'is_author': is_author},
    )


@login_required
def post_delete(request, post_id):
    """Функция обрабатывает запрос на удаление статьи из базы."""
    post = get_object_or_404(Post, id=post_id)
    post_user_id = post.user.id
    if request.user != post.user:
        return redirect('err403')
    if request.method == 'POST':
        post.delete()
        return redirect('user_post_view', user_id=post_user_id)
    return render(request, 'posts/post_delete.html', {'post': post})


@login_required
def new_post(request):
    """Функция генерит форму для создания новой статьи,
    получает данные из формы и сохраняет в базе данных."""
    if request.method != 'POST':
        form = PostForm()
        return render(request, 'posts/new.html', {'form': form})
    form = PostForm(request.POST, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect('user_post_view', user_id=request.user.id)
    return render(request, 'posts/new.html', {'form': form})


def page_not_found(request, exception=None):
    """Функция возвращает сгенерированную страницу для ошибки 404."""
    return render(
        request,
        'posts/misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    """Функция возвращает сгенерированную страницу для ошибки 500."""
    return render(request, 'posts/misc/500.html', status=500)


def forbidden_action(request):
    """Функция возвращает сгенерированную страницу для ошибки 403."""
    return render(request, 'posts/misc/403.html', status=403)
