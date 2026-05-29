from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("jobs/", views.jobs, name="jobs"),
    path("schemes/", views.schemes, name="schemes"),
    path("scholarships/", views.scholarships, name="scholarships"),
    path("ai-assistant/", views.ai_assistant, name="ai-assistant"),
]

