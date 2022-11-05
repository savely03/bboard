from django.contrib import admin
from .models import AvdUser, SubRubric, SuperRubric, Bb, AdditionalImage, Comment
from .forms import SubRubricForm


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


class SubRubricInline(admin.TabularInline):
    model = SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
    inlines = (SubRubricInline,)


class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm


class AdditionalInline(admin.TabularInline):
    model = AdditionalImage


class BbAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'content', 'author', 'created_at')
    list_display_links = ('rubric', 'title')
    inlines = (AdditionalInline,)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('bb', 'author', 'is_active')
    list_display_links = ('bb', 'author')


admin.site.register(SuperRubric, SuperRubricAdmin)

admin.site.register(AvdUser, AdvUserAdmin)

admin.site.register(SubRubric, SubRubricAdmin)

admin.site.register(Bb, BbAdmin)

admin.site.register(Comment, CommentAdmin)
