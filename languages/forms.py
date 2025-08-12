# languages/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# If you're using django-allauth (you are), extend its SignupForm
from allauth.account.forms import SignupForm as AllauthSignupForm

from .models import Booking, Profile

User = get_user_model()

ROLE_CHOICES = (
    ("student", "Student"),
    ("tutor", "Tutor"),
)


class BookingForm(forms.ModelForm):
    """
    Booking form for your Booking model.
    Validates that a user can't book the same course twice.
    NOTE: Ensure these fields exist on your Booking model.
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
        self.user = user  # pass from the view

    def clean(self):
        cleaned = super().clean()
        course = cleaned.get("course")

        # Duplicate booking check (only if we have a logged-in user and a course)
        if self.user and course:
            qs = Booking.objects.filter(user=self.user, course=course)
            # Exclude self when editing
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("You already booked this course.")

        return cleaned


class RoleSignupForm(AllauthSignupForm):
    """
    Allauth-compatible signup form that adds a 'role' field and writes it to Profile.
    Wire it in settings.py:
        ACCOUNT_FORMS = {"signup": "languages.forms.RoleSignupForm"}
    """
    role = forms.ChoiceField(choices=ROLE_CHOICES, initial="student")

    def save(self, request):
        # Create the user via allauth first
        user = super().save(request)

        # Ensure Profile exists, then set the role
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = self.cleaned_data.get("role", "student")
        profile.save()

        return user