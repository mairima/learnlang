# languages/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm as AllauthSignupForm

from .models import Booking, Profile, Course

User = get_user_model()


class BookingForm(forms.ModelForm):
    """
    Booking form for Booking model (no date/time fields).
    - Orders course dropdown by start_date then title
    - Validates: a user can't book the same course twice
    """
    class Meta:
        model = Booking
        fields = ["course", "name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address (optional)"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Anything you'd like to add?"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # set by the view
        # Populate & order the course select
        self.fields["course"].queryset = Course.objects.order_by("start_date", "title")
        self.fields["course"].widget.attrs.update({"class": "form-select"})

    def clean(self):
        cleaned = super().clean()
        course = cleaned.get("course")

        # Duplicate booking check (only if logged in and a course selected)
        if self.user and course:
            qs = Booking.objects.filter(user=self.user, course=course)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("You already booked this course.")

        return cleaned


class RoleSignupForm(AllauthSignupForm):
    """
    Allauth signup form: force role = student (hidden) + Bootstrap styling.
    """
    role = forms.CharField(widget=forms.HiddenInput(), initial="student")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_cfg = {
            "email":     {"placeholder": "Email address",    "autocomplete": "email"},
            "username":  {"placeholder": "Username",         "autocomplete": "username"},
            "password1": {"placeholder": "Password",         "autocomplete": "new-password"},
            "password2": {"placeholder": "Password (again)", "autocomplete": "new-password"},
        }
        for name, cfg in field_cfg.items():
            if name in self.fields:
                self.fields[name].widget.attrs.update({"class": "form-control", **cfg})

        first = next((n for n in ("email", "username") if n in self.fields), None)
        if first:
            self.fields[first].widget.attrs.setdefault("autofocus", True)

    def clean_username(self):
        username = super().clean_username()
        return username.strip()

    def clean_email(self):
        email = super().clean_email()
        return email.strip().lower()

    def save(self, request):
        user = super().save(request)
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = "student"  # enforce student
        profile.save()
        return user
