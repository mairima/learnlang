# languages/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm as AllauthSignupForm  # ok to keep; remove if unused

from .models import Booking, Profile, Course, ContactMessage

User = get_user_model()


def _display_name_for(user):
    """Pick a nice display name from the logged-in user."""
    full = f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip()
    if full:
        return full
    prof = getattr(user, "profile", None)
    # If you later add profile.display_name, prefer it here, e.g.:
    # if prof and getattr(prof, "display_name", ""):
    #     return prof.display_name
    return getattr(user, "username", None) or getattr(user, "email", "")


class BookingForm(forms.ModelForm):
    """
    Booking form for Booking model (no date/time fields).
    - Orders course dropdown by start_date then title
    - Validates: a user can't book the same course twice
    - For authenticated users: hide name field and set it automatically
    """
    class Meta:
        model = Booking
        fields = ["course", "name", "email", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email address",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Anything you'd like to add?",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # set by the view

        # Populate & order the course select
        self.fields["course"].queryset = Course.objects.order_by("start_date", "title")
        self.fields["course"].widget.attrs.update({"class": "form-select"})

        # Email is mandatory for everyone
        self.fields["email"].required = True

        # If a user is logged in, do NOT ask for name again.
        if self.user and getattr(self.user, "is_authenticated", False):
            # remove name from rendered form; we'll set it in save()
            self.fields.pop("name")
            # prefill email from account for convenience (still required)
            if getattr(self.user, "email", "") and "email" not in self.initial:
                self.initial["email"] = self.user.email

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

    def save(self, commit=True):
        """Ensure 'name' is always set from logged-in user; email remains required."""
        booking = super().save(commit=False)
        if self.user and getattr(self.user, "is_authenticated", False):
            booking.name = _display_name_for(self.user)
        if commit:
            booking.save()
        return booking


class ContactForm(forms.ModelForm):
    """Minimal contact form that saves to ContactMessage so admins can read it."""
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "How can we help?"}),
        }
