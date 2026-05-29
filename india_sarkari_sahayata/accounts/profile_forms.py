from django import forms

from .models import CandidateProfile


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ["full_name", "profile_image", "education"]
        widgets = {
            "education": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base = (
            "w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm "
            "outline-none ring-brand-100 transition focus:border-brand-600 focus:ring-4"
        )
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {base}".strip()
