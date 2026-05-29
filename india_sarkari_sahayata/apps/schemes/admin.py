from django.contrib import admin

from .models import Scheme, SchemeCategory


@admin.register(SchemeCategory)
class SchemeCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "state", "is_active", "updated_at")
    list_filter = ("is_active", "state", "category")
    search_fields = ("title", "summary", "description", "ministry_or_department")
    prepopulated_fields = {"slug": ("title",)}
