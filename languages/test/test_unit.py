# languages/tests/test_unit.py
from datetime import timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from languages.models import Course, Booking, ContactMessage
from languages.forms import BookingForm, _display_name_for

User = get_user_model()


class BookingFormUnitTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="alice", email="alice@example.com", password="pass123",
            first_name="Alice", last_name="Smith"
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

        u2 = User.objects.create_user(username="bob", email="bob@example.com", password="x")
        self.assertEqual(_display_name_for(u2), "bob")  # falls back to username

    def test_booking_form_prefills_for_logged_in_user(self):
        """Name and email are prefilled for authenticated users (but name remains visible)."""
        form = BookingForm(user=self.user)
        # booking form sets initial values for logged in user
        self.assertEqual(form.initial.get("name"), "Alice Smith")
        self.assertEqual(form.initial.get("email"), "alice@example.com")
        # email is required for everyone
        self.assertTrue(form.fields["email"].required)

    def test_booking_form_duplicate_booking_blocked(self):
        """The same user cannot book the same course twice."""
        # Existing booking
        Booking.objects.create(
            user=self.user, course=self.course, name="Alice Smith", email="alice@example.com"
        )

        # Try to book same course again
        data = {
            "course": self.course.pk,
            "name": "Alice Smith",
            "email": "alice@example.com",
            "message": "Second try",
        }
        form = BookingForm(data=data, user=self.user)
        self.assertFalse(form.is_valid())
        # Non-field error raised in clean()
        self.assertIn("You already booked this course.", str(form.errors))

    def test_booking_form_save_sets_authoritative_name(self):
        """Even if name is altered in the POST, save() uses the logged-in account name."""
        data = {
            "course": self.course.pk,
            "name": "Hacked Name",  # attempt to spoof
            "email": "alice@example.com",
            "message": "Hello",
        }
        form = BookingForm(data=data, user=self.user)
        self.assertTrue(form.is_valid(), form.errors)
        booking = form.save()
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.course, self.course)
        # Name must come from the user account, not the POSTed value
        self.assertEqual(booking.name, "Alice Smith")


class ContactFormAndViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="carol", email="carol@example.com", password="pass123"
        )

    def test_contact_post_logged_out(self):
        url = reverse("contact_us")
        payload = {
            "name": "Guest User",
            "email": "guest@example.com",
            "subject": "Info",
            "message": "How do I book?",
        }
        before = ContactMessage.objects.count()
        resp = self.client.post(url, payload, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), before + 1)
        msg = ContactMessage.objects.latest("created_at")
        self.assertIsNone(msg.user)  # no user attached
        self.assertEqual(msg.name, "Guest User")
        self.assertEqual(msg.email, "guest@example.com")

    def test_contact_post_logged_in(self):
        self.client.force_login(self.user)
        url = reverse("contact_us")
        payload = {
            "name": "",  # let the view fill from user if blank
            "email": "",  # let the view fill from user if blank
            "subject": "Support",
            "message": "Please assist.",
        }
        before = ContactMessage.objects.count()
        resp = self.client.post(url, payload, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), before + 1)
        msg = ContactMessage.objects.latest("created_at")
        self.assertEqual(msg.user, self.user)
        self.assertEqual(msg.email, "carol@example.com")


class MyBookingsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="dave", email="dave@example.com", password="pass123",
            first_name="Dave", last_name="Jones"
        )
        today = timezone.now().date()
        self.course = Course.objects.create(
            title="English B1",
            capacity=10,
            start_date=today,
            end_date=today + timedelta(days=10),
        )
        self.booking = Booking.objects.create(
            user=self.user, course=self.course, name="Dave Jones", email="dave@example.com"
        )

    def test_my_bookings_requires_login_and_lists_booking(self):
        # not logged in → redirect to login
        url = reverse("my_bookings")
        resp = self.client.get(url)
        self.assertIn(resp.status_code, (302, 301))

        # logged in
        self.client.force_login(self.user)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # context contains our booking
        bookings = resp.context.get("bookings")
        self.assertIsNotNone(bookings)
        self.assertTrue(bookings.filter(pk=self.booking.pk).exists())
