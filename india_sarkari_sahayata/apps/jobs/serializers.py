from rest_framework import serializers

from .models import SavedJob


class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = [
            "id",
            "title",
            "company",
            "location",
            "source",
            "external_id",
            "url",
            "published_at",
            "is_featured",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class ExternalJobSerializer(serializers.Serializer):
    external_id = serializers.CharField()
    title = serializers.CharField()
    company = serializers.CharField(allow_blank=True)
    location = serializers.CharField(allow_blank=True)
    url = serializers.URLField()
    source = serializers.CharField()
    published_at = serializers.DateTimeField(allow_null=True)

