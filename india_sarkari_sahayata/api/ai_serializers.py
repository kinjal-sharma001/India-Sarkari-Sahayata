from rest_framework import serializers


class ResumeAnalyzerSerializer(serializers.Serializer):
    resume_text = serializers.CharField(min_length=80, max_length=20000)


class SchemeRecommendationSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=14, max_value=100)
    category = serializers.CharField(max_length=60)
    income = serializers.FloatField(min_value=0)
    education = serializers.CharField(max_length=200)


class CareerChatSerializer(serializers.Serializer):
    question = serializers.CharField(min_length=5, max_length=2000)
    education = serializers.CharField(max_length=200, required=False, allow_blank=True)
    age = serializers.IntegerField(min_value=14, max_value=100, required=False)
    category = serializers.CharField(max_length=60, required=False, allow_blank=True)
    income = serializers.FloatField(min_value=0, required=False)
    history = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        required=False,
        allow_empty=True,
    )
