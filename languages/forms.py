# languages/forms.py
from django import forms
from django.core.exceptions import ValidationError

from .models import Booking, Course, ContactMessage


def _display_name_for(user):
    """Pick a nice display name from the logged-in user."""
    first = getattr(user, "first_name", "") or ""
    last = getattr(user, "last_name", "") or ""
    full = (first + " " + last).strip()
    if full:
        return full
    # If you later add profile.display_name, prefer it here.
    # prof = getattr(user, "profile", None)
    # if prof and getattr(prof, "display_name", ""):
    #     return prof.display_name
    username = getattr(user, "username", None)
    email = getattr(user, "email", "")
    return username or email


class BookingForm(forms.ModelForm):
    """
    Booking form for Booking model (no date/time fields).
    - Orders course dropdown by start_date then title
    - Validates: a user cannot book the same course twice
    - For authenticated users: show name prefilled (not hidden)
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
                    "placeholder": "Anything you would like to add?",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # set by the view

        # Populate and order the course select
        self.fields["course"].queryset = Course.objects.order_by(
            "start_date", "title"
        )
        self.fields["course"].widget.attrs.update({"class": "form-select"})

        # Email is mandatory for everyone
        self.fields["email"].required = True

        # If logged in, prefill (do not hide the name field)
        if self.user and getattr(self.user, "is_authenticated", False):
            display_name = _display_name_for(self.user)
            if display_name and "name" not in self.initial:
                self.initial["name"] = display_name
            if getattr(self.user, "email", "") and "email" not in self.initial:
                self.initial["email"] = self.user.email

    def clean(self):
        cleaned = super().clean()
        course = cleaned.get("course")

        # Duplicate booking check (only if logged in and course selected)
        if self.user and course:
            qs = Booking.objects.filter(user=self.user, course=course)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("You already booked this course.")
        return cleaned

    def save(self, commit=True):
        """Ensure 'name' is set from logged-in user; email stays required."""
        booking = super().save(commit=False)
        if self.user and getattr(self.user, "is_authenticated", False):
            # Persist authoritative account name regardless of form edits
            booking.name = _display_name_for(self.user)
        if commit:
            booking.save()
        return booking


class ContactForm(forms.ModelForm):
    """Minimal contact form that saves to ContactMessage for admins."""

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
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
                    "placeholder": "you@example.com",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Subject",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "How can we help?",
                }
            ),
        }
