# languages/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# django-allauth
from allauth.account.forms import SignupForm as AllauthSignupForm

from .models import Booking, Profile, Course

User = get_user_model()


class BookingForm(forms.ModelForm):
    """
    Booking form for Booking model.
    - Orders course dropdown by start_date then title
    - Validates: a user can't book the same course twice
    """
    class Meta:
        model = Booking
        fields = ["course", "name", "email", "date", "time", "message"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # set by the view
        # Populate and order the course dropdown
        self.fields["course"].queryset = Course.objects.order_by("start_date", "title")

    def clean(self):
        cleaned = super().clean()
        course = cleaned.get("course")

        # Prevent duplicate booking of the same course by the same user
        if self.user and course:
            qs = Booking.objects.filter(user=self.user, course=course)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("You already booked this course.")
        return cleaned


class RoleSignupForm(AllauthSignupForm):
    """
    Allauth signup form without any role choice UI.
    Every new user is assigned the 'student' role.
    (Make sure settings.py has:
        ACCOUNT_FORMS = {"signup": "languages.forms.RoleSignupForm"}
    )
    """
    def save(self, request):
        user = super().save(request)
        profile, _ = Profile.objects.get_or_create(user=user, defaults={"role": "student"})
        # If it existed already, still enforce student role
        if profile.role != "student":
            profile.role = "student"
            profile.save()
        return user
