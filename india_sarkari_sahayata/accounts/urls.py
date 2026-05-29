from django.urls import path

from .views import (
    login_view,
    logout_view,
    profile_view,
    register_view,
    toggle_saved_job_view,
    toggle_saved_scholarship_view,
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/saved-jobs/<int:job_id>/toggle/", toggle_saved_job_view, name="toggle-saved-job"),
    path(
        "profile/saved-scholarships/<int:scholarship_id>/toggle/",
        toggle_saved_scholarship_view,
        name="toggle-saved-scholarship",
    ),
]
