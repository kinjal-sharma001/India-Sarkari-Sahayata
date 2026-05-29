from django.urls import path

from .views import (
    create_resume_view,
    download_resume_pdf_view,
    edit_resume_view,
    my_resumes_view,
    preview_resume_view,
    resume_analyzer_view,
)

urlpatterns = [
    path("", my_resumes_view, name="my-resumes"),
    path("create/", create_resume_view, name="resume-create"),
    path("analyzer/", resume_analyzer_view, name="resume-analyzer"),
    path("analyzer/<int:resume_id>/", resume_analyzer_view, name="resume-analyzer-resume"),
    path("preview/<int:resume_id>/", preview_resume_view, name="resume-preview"),
    path("download/<int:resume_id>/", download_resume_pdf_view, name="resume-download"),
    path("edit/<int:resume_id>/", edit_resume_view, name="resume-edit"),
]
