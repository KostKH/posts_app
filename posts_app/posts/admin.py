from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    """Класс нужен для вывода на странице админа
    детальной информации по публикациям."""

    list_display = (
        'id',
        'title',
        'body',
        'user',
    )
    search_fields = ('title', 'body',)
    list_filter = ('id', 'user')
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
