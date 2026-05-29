from django.db import models
from django.utils.text import slugify


class SchemeCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Scheme categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Scheme(models.Model):
    class State(models.TextChoices):
        ALL_INDIA = "ALL", "All India"
        ANDHRA_PRADESH = "AP", "Andhra Pradesh"
        ASSAM = "AS", "Assam"
        BIHAR = "BR", "Bihar"
        DELHI = "DL", "Delhi"
        GUJARAT = "GJ", "Gujarat"
        HARYANA = "HR", "Haryana"
        KARNATAKA = "KA", "Karnataka"
        KERALA = "KL", "Kerala"
        MADHYA_PRADESH = "MP", "Madhya Pradesh"
        MAHARASHTRA = "MH", "Maharashtra"
        ODISHA = "OD", "Odisha"
        PUNJAB = "PB", "Punjab"
        RAJASTHAN = "RJ", "Rajasthan"
        TAMIL_NADU = "TN", "Tamil Nadu"
        TELANGANA = "TS", "Telangana"
        UTTAR_PRADESH = "UP", "Uttar Pradesh"
        WEST_BENGAL = "WB", "West Bengal"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    summary = models.CharField(max_length=280, blank=True)
    description = models.TextField(blank=True)

    category = models.ForeignKey(
        SchemeCategory, on_delete=models.PROTECT, related_name="schemes"
    )
    ministry_or_department = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=3, choices=State.choices, default=State.ALL_INDIA)

    eligibility = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    application_url = models.URLField(blank=True)
    tags = models.JSONField(default=list, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "title"]
        indexes = [
            models.Index(fields=["is_active", "state"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
