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