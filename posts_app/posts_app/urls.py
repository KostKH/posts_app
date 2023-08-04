from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('api/', include('api.urls')),
    path('', include('posts.urls')),
]
handler404 = 'posts.views.page_not_found'
handler500 = 'posts.views.server_error'
