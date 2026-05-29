from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import JobSearchAPIView
from .viewsets import SavedJobViewSet

app_name = "jobs"

router = DefaultRouter()
router.register(r"", SavedJobViewSet, basename="job")

urlpatterns = [
    path("search/", JobSearchAPIView.as_view(), name="job-search"),
    path("", include(router.urls)),
]
