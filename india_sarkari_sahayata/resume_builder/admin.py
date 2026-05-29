from django.contrib import admin

from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("full_name", "email", "user__username", "skills", "education")
