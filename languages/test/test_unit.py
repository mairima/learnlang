# languages/tests/test_unit.py
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from languages.forms import BookingForm, _display_name_for
from languages.models import Booking, ContactMessage, Course

User = get_user_model()


class BookingFormUnitTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="pass123",
            first_name="Alice",
            last_name="Smith",
        )
        today = timezone.now().date()
        self.course = Course.objects.create(
            title="English A1",
            capacity=10,
            start_date=today,
            end_date=today + timedelta(days=7),
        )

    def test__display_name_for_prefers_full_name(self):
        """_display_name_for returns first+last over username/email."""
        self.assertEqual(_display_name_for(self.user), "Alice Smith")

        u2 = User.objects.create_user(
            username="bob", email="bob@example.com", password="x"
        )
        # falls back to username
        self.assertEqual(_display_name_for(u2), "bob")

    def test_booking_form_prefills_for_logged_in_user(self):
        """
        Name and email are prefilled for authenticated users
        (but name remains visible).
        """
        form = BookingForm(user=self.user)
        self.assertEqual(form.initial.get("name"), "Alice Smith")
        self.assertEqual(form.initial.get("email"), "alice@example.com")
        self.assertTrue(form.fields["email"].required)

    def test_booking_form_duplicate_booking_blocked(self):
        """The same user cannot book the same course twice."""
        Booking.objects.create(
            user=self.user,
            course=self.course,
            name="Alice Smith",
            email="alice@example.com",
        )

        data = {
            "course": self.course.pk,
            "name": "Alice Smith",
            "email": "alice@example.com",
            "message": "Second try",
        }
        form = BookingForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("You already booked this course.", str(form.errors))

    def test_booking_form_save_sets_authoritative_name
