from django.contrib import admin

from .models import Scholarship


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "provider", "level", "deadline", "is_active", "updated_at")
    list_filter = ("is_active", "category", "level")
    search_fields = ("title", "provider", "summary", "description", "eligibility")
    prepopulated_fields = {"slug": ("title",)}
