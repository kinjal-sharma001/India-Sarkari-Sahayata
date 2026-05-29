from django.urls import include, path

urlpatterns = [
    path("jobs/", include("apps.jobs.urls")),
    path("schemes/", include("apps.schemes.urls")),
    path("scholarships/", include("apps.scholarships.urls")),
    path("ai/", include("api.ai_urls")),
]

