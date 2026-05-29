from rest_framework import viewsets

from .filters import SchemeFilter
from .models import Scheme, SchemeCategory
from .serializers import SchemeCategorySerializer, SchemeSerializer


class SchemeCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SchemeCategory.objects.all()
    serializer_class = SchemeCategorySerializer
    search_fields = ["name", "slug"]


class SchemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Scheme.objects.select_related("category").all()
    serializer_class = SchemeSerializer
    filterset_class = SchemeFilter
    search_fields = ["title", "summary", "description", "eligibility", "benefits", "ministry_or_department"]
    ordering_fields = ["updated_at", "created_at", "title"]
    ordering = ["-updated_at"]

