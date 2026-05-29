from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import ScholarshipViewSet

app_name = "scholarships"

router = DefaultRouter()
router.register(r"", ScholarshipViewSet, basename="scholarship")

urlpatterns = [
    path("", include(router.urls)),
]
