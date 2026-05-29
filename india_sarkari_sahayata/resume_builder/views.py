from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .forms import ResumeForm
from .models import Resume


def _compose_resume_text(resume: Resume) -> str:
    parts = [
        f"Name: {resume.full_name}",
        f"Email: {resume.email}",
        f"Phone: {resume.phone}" if resume.phone else "",
        f"LinkedIn: {resume.linkedin}" if resume.linkedin else "",
        f"GitHub: {resume.github}" if resume.github else "",
        f"Summary:\n{resume.summary}" if resume.summary else "",
        f"Education:\n{resume.education}" if resume.education else "",
        f"Skills:\n{resume.skills}" if resume.skills else "",
        f"Experience:\n{resume.experience}" if resume.experience else "",
        f"Projects:\n{resume.projects}" if resume.projects else "",
    ]
    return "\n\n".join([part for part in parts if part])


@login_required
def create_resume_view(request):
    form = ResumeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        resume = form.save(commit=False)
        resume.user = request.user
        resume.save()
        messages.success(request, "Resume created successfully.")
        return redirect("resume-preview", resume_id=resume.id)
    return render(request, "resume_builder/resume_form.html", {"form": form, "mode": "create"})


@login_required
def my_resumes_view(request):
    resumes = Resume.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "resume_builder/my_resumes.html", {"resumes": resumes})


@login_required
def edit_resume_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    form = ResumeForm(request.POST or None, instance=resume)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Resume updated successfully.")
        return redirect("resume-preview", resume_id=resume.id)
    return render(
        request,
        "resume_builder/resume_form.html",
        {"form": form, "resume": resume, "mode": "edit"},
    )


@login_required
def preview_resume_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    return render(request, "resume_builder/resume_preview.html", {"resume": resume})


@login_required
def resume_analyzer_view(request, resume_id=None):
    selected_resume = None
    prefilled_text = ""
    if resume_id is not None:
        selected_resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        prefilled_text = _compose_resume_text(selected_resume)
    resumes = Resume.objects.filter(user=request.user).only("id", "full_name")
    return render(
        request,
        "resume_builder/resume_analyzer.html",
        {
            "resumes": resumes,
            "selected_resume": selected_resume,
            "prefilled_text": prefilled_text,
        },
    )


@login_required
def download_resume_pdf_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="resume_{resume.id}.pdf"'
    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    x = 48
    y = height - 50

    def draw_heading(text: str):
        nonlocal y
        if y < 80:
            pdf.showPage()
            y = height - 50
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(x, y, text)
        y -= 18

    def draw_body(text: str):
        nonlocal y
        if not text:
            return
        pdf.setFont("Helvetica", 10)
        lines = str(text).splitlines() or [""]
        for line in lines:
            chunks = [line[i : i + 100] for i in range(0, len(line), 100)] or [""]
            for chunk in chunks:
                if y < 60:
                    pdf.showPage()
                    y = height - 50
                    pdf.setFont("Helvetica", 10)
                pdf.drawString(x, y, chunk)
                y -= 14
        y -= 6

    draw_heading(resume.full_name)
    draw_body(f"Email: {resume.email}")
    if resume.phone:
        draw_body(f"Phone: {resume.phone}")
    if resume.linkedin:
        draw_body(f"LinkedIn: {resume.linkedin}")
    if resume.github:
        draw_body(f"GitHub: {resume.github}")
    draw_body("")

    sections = [
        ("Professional Summary", resume.summary),
        ("Education", resume.education),
        ("Skills", resume.skills),
        ("Experience", resume.experience),
        ("Projects", resume.projects),
    ]
    for title, value in sections:
        if value:
            draw_heading(title)
            draw_body(value)

    pdf.showPage()
    pdf.save()
    return response
