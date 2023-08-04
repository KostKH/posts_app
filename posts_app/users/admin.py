from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import Group, UserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class MyUserAdmin(UserAdmin):
    '''Класс для вывода на странице админа
    информации о пользователе.'''
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Personal info'),
            {
                'fields': (
                    'name',
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'name',
                           'password1', 'password2', 'latitude',
                           'longitude',),
            },
        ),
    )
    list_display = (
        'id',
        'email',
        'name',
        'is_staff',
    )
    list_filter = ('email',)
    ordering = ('email',)
    search_fields = ('name', 'email')


admin.site.register(User, MyUserAdmin)
admin.site.unregister(Group)
