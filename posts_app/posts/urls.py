from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/<int:user_id>/posts/',
         views.user_post_view,
         name='user_post_view'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('posts/new/', views.new_post, name='new_post'),
    path('404/', views.page_not_found, name='err404'),
    path('500/', views.server_error, name='err500'),
    path('403/', views.forbidden_action, name='err403'),
]
