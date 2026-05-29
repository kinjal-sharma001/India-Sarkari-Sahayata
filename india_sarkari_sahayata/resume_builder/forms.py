from django import forms

from .models import Resume


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            "full_name",
            "email",
            "phone",
            "summary",
            "education",
            "skills",
            "experience",
            "projects",
            "linkedin",
            "github",
        ]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 4}),
            "education": forms.Textarea(attrs={"rows": 4}),
            "skills": forms.Textarea(attrs={"rows": 4}),
            "experience": forms.Textarea(attrs={"rows": 5}),
            "projects": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = (
            "w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm "
            "outline-none ring-brand-100 transition focus:border-brand-600 focus:ring-4"
        )
        for field_name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base_class}".strip()
            field.widget.attrs.setdefault("id", f"id_{field_name}")

        self.fields["full_name"].widget.attrs.setdefault("placeholder", "Enter your full name")
        self.fields["email"].widget.attrs.setdefault("placeholder", "Enter email")
        self.fields["phone"].widget.attrs.setdefault("placeholder", "Enter phone number")
        self.fields["linkedin"].widget.attrs.setdefault("placeholder", "LinkedIn profile URL")
        self.fields["github"].widget.attrs.setdefault("placeholder", "GitHub profile URL")
