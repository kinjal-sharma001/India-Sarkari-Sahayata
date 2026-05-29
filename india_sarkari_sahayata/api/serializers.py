from rest_framework import serializers

from apps.scholarships.models import Scholarship
from apps.schemes.models import Scheme


class SchemeSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Scheme
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "description",
            "category",
            "category_display",
            "ministry_or_department",
            "state",
            "eligibility",
            "benefits",
            "application_url",
            "tags",
            "is_active",
        ]
        read_only_fields = ["id", "slug", "is_active", "created_at", "updated_at"]


class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "provider",
            "level",
            "summary",
            "description",
            "eligibility",
            "amount",
            "deadline",
            "application_url",
            "tags",
            "is_active",
        ]
        read_only_fields = ["id", "slug", "is_active", "created_at", "updated_at"]

