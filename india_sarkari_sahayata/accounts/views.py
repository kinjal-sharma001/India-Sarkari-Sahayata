from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import CandidateLoginForm, CandidateRegistrationForm
from .models import CandidateProfile
from .profile_forms import CandidateProfileForm
from apps.jobs.models import SavedJob
from apps.scholarships.models import Scholarship


def _get_safe_next(request):
    next_url = request.POST.get("next") or request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return next_url
    return reverse("home")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = CandidateRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Registration successful. Welcome to your dashboard.")
        return redirect(_get_safe_next(request))
    return render(request, "accounts/register.html", {"form": form, "next": request.GET.get("next", "")})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = CandidateLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:
            form.add_error(None, "Invalid username or password.")
        else:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect(_get_safe_next(request))
    return render(request, "accounts/login.html", {"form": form, "next": request.GET.get("next", "")})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out.")
    return redirect("login")


@login_required
def profile_view(request):
    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = CandidateProfileForm(instance=profile)
    context = {
        "form": form,
        "profile": profile,
        "saved_jobs": profile.saved_jobs.all()[:20],
        "saved_scholarships": profile.saved_scholarships.all()[:20],
    }
    return render(request, "accounts/profile.html", context)


@login_required
def toggle_saved_job_view(request, job_id):
    if request.method != "POST":
        return redirect("profile")
    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
    job = get_object_or_404(SavedJob, id=job_id)
    if profile.saved_jobs.filter(id=job.id).exists():
        profile.saved_jobs.remove(job)
        messages.info(request, "Job removed from saved list.")
    else:
        profile.saved_jobs.add(job)
        messages.success(request, "Job saved to your profile.")
    return redirect("profile")


@login_required
def toggle_saved_scholarship_view(request, scholarship_id):
    if request.method != "POST":
        return redirect("profile")
    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
    if profile.saved_scholarships.filter(id=scholarship.id).exists():
        profile.saved_scholarships.remove(scholarship)
        messages.info(request, "Scholarship removed from saved list.")
    else:
        profile.saved_scholarships.add(scholarship)
        messages.success(request, "Scholarship saved to your profile.")
    return redirect("profile")
