from django.contrib import admin
from .models import CandidateProfile


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "updated_at")
    search_fields = ("user__username", "user__email", "full_name")
    filter_horizontal = ("saved_jobs", "saved_scholarships")
