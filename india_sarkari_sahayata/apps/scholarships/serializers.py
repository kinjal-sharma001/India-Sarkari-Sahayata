from rest_framework import serializers

from .models import Scholarship


class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = [
            "id",
            "title",
            "category",
            "slug",
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
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

