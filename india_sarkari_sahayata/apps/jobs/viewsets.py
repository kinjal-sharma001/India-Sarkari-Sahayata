from rest_framework import viewsets

from .models import SavedJob
from .serializers import SavedJobSerializer


class SavedJobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SavedJob.objects.all()
    serializer_class = SavedJobSerializer
    search_fields = ["title", "company", "location", "source"]
    ordering_fields = ["created_at", "published_at", "title"]
    ordering = ["-is_featured", "-created_at"]

