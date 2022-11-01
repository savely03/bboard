from django.contrib import admin
from .models import AvdUser


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fields = (
        ('username', 'email'),
        ('first_name', 'last_name'),
        ('send_messages', 'is_activated', 'is_active'),
        ('is_staff', 'is_superuser'),
        ('groups', 'user_permissions'),
        ('last_login', 'date_joined')
    )
    readonly_fields = ('last_login', 'date_joined')


admin.site.register(AvdUser, AdvUserAdmin)
