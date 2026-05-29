from django.db import models


class SavedJob(models.Model):
    """
    Optional persistence layer for jobs the admin wants to feature/bookmark.
    External job search remains API-driven (not hardcoded).
    """

    title = models.CharField(max_length=220)
    company = models.CharField(max_length=180, blank=True)
    location = models.CharField(max_length=180, blank=True)
    source = models.CharField(max_length=60, default="external")
    external_id = models.CharField(max_length=120, blank=True)
    url = models.URLField()
    published_at = models.DateTimeField(null=True, blank=True)

    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]
        indexes = [
            models.Index(fields=["is_featured", "created_at"]),
            models.Index(fields=["external_id"]),
        ]

    def __str__(self) -> str:
        return self.title
