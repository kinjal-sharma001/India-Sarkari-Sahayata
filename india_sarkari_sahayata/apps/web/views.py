from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from resume_builder.models import Resume


@login_required
def home(request):
    my_resumes = Resume.objects.filter(user=request.user).only("id", "full_name", "created_at")[:5]
    return render(request, "web/home.html", {"my_resumes": my_resumes})


@login_required
def jobs(request):
    return render(request, "web/jobs.html")


@login_required
def schemes(request):
    return render(request, "web/schemes.html")


@login_required
def scholarships(request):
    return render(request, "web/scholarships.html")


@login_required
def ai_assistant(request):
    return render(request, "web/ai_assistant.html")
