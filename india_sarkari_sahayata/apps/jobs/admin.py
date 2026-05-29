from django.contrib import admin

from .models import SavedJob


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "source", "is_featured", "created_at")
    list_filter = ("is_featured", "source")
    search_fields = ("title", "company", "location", "url", "external_id")
