from rest_framework import viewsets

from .filters import ScholarshipFilter
from .models import Scholarship
from .serializers import ScholarshipSerializer


class ScholarshipViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    filterset_class = ScholarshipFilter
    search_fields = ["title", "category", "provider", "summary", "description", "eligibility"]
    ordering_fields = ["updated_at", "created_at", "deadline", "title"]
    ordering = ["-updated_at"]

