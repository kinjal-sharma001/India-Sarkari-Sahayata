from django.urls import path

from .ai_views import (
    AICareerChatbotAPIView,
    AIResumeAnalyzerAPIView,
    AISchemeRecommendationAPIView,
)

urlpatterns = [
    path("resume-analyzer/", AIResumeAnalyzerAPIView.as_view(), name="ai-resume-analyzer"),
    path(
        "scheme-recommendation/",
        AISchemeRecommendationAPIView.as_view(),
        name="ai-scheme-recommendation",
    ),
    path("career-chat/", AICareerChatbotAPIView.as_view(), name="ai-career-chat"),
]
