from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class TailwindStyledMixin:
    # Applies professional Tailwind CSS styling to form fields.
    base_input_class = (
        "w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-sm "
        "outline-none ring-brand-100 transition focus:border-brand-600 focus:ring-4"
    )

    def apply_tailwind_classes(self) -> None:
        for field_name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {self.base_input_class}".strip()
            field.widget.attrs.setdefault("id", f"id_{field_name}")


class CandidateRegistrationForm(TailwindStyledMixin, UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "placeholder": "Enter your email",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind_classes()
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "Choose a username",
                "autocomplete": "username",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": "Create password",
                "autocomplete": "new-password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": "Confirm password",
                "autocomplete": "new-password",
            }
        )

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if not email:
            raise ValidationError("Email is required.")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CandidateLoginForm(TailwindStyledMixin, AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autofocus": True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind_classes()
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "Username",
                "autocomplete": "username",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        )
