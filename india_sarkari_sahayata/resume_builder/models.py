from django.contrib.auth.models import User
from django.db import models


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resumes")
    full_name = models.CharField(max_length=180)
    email = models.EmailField()
    phone = models.CharField(max_length=25, blank=True)
    summary = models.TextField(blank=True)
    education = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.full_name} ({self.user.username})"
