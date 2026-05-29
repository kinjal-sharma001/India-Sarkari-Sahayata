from rest_framework import serializers

from .models import Scheme, SchemeCategory


class SchemeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeCategory
        fields = ["id", "name", "slug"]


class SchemeSerializer(serializers.ModelSerializer):
    category = SchemeCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category", queryset=SchemeCategory.objects.all(), write_only=True
    )

    class Meta:
        model = Scheme
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "description",
            "category",
            "category_id",
            "ministry_or_department",
            "state",
            "eligibility",
            "benefits",
            "application_url",
            "tags",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

