from django.contrib.auth.models import User
from django.db import models


class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="candidate_profile")
    full_name = models.CharField(max_length=180, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    education = models.TextField(blank=True)
    saved_jobs = models.ManyToManyField("jobs.SavedJob", blank=True, related_name="saved_by_profiles")
    saved_scholarships = models.ManyToManyField(
        "scholarships.Scholarship",
        blank=True,
        related_name="saved_by_profiles",
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return self.full_name or self.user.username
