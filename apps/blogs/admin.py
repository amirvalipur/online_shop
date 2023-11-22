from django.contrib import admin
from .models import Blog, Author
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(Blog)
class BlogAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['blog_title', 'author', 'convert_date_time', 'is_active']
    list_filter = ['blog_title', 'author', 'is_active']
    search_fields = ['blog_title', 'author']
    ordering = ['author', 'is_active']
    list_editable = ['is_active']
