from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import SchemeCategoryViewSet, SchemeViewSet

app_name = "schemes"

router = DefaultRouter()
router.register(r"categories", SchemeCategoryViewSet, basename="scheme-category")
router.register(r"", SchemeViewSet, basename="scheme")

urlpatterns = [
    path("", include(router.urls)),
]
