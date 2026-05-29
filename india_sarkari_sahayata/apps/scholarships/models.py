from django.db import models
from django.utils.text import slugify


class Scholarship(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=260, unique=True, blank=True)
    category = models.CharField(max_length=120, blank=True)
    provider = models.CharField(max_length=200, blank=True)
    level = models.CharField(max_length=120, blank=True)  # e.g. School/UG/PG/PhD

    summary = models.CharField(max_length=280, blank=True)
    description = models.TextField(blank=True)
    eligibility = models.TextField(blank=True)

    amount = models.CharField(max_length=120, blank=True)  # keep flexible (₹ / stipend)
    deadline = models.DateField(null=True, blank=True)
    application_url = models.URLField(blank=True)

    tags = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "title"]
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["deadline"]),
            models.Index(fields=["category"]),
            models.Index(fields=["level"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
