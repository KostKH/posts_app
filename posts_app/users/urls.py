from django.contrib.auth import views as auth_views
from django.urls import path

from .views import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
]
