# languages/test_booking_happy_path.py
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from languages.models import Course, Booking

User = get_user_model()


class BookingHappyPathTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alice",
            password="secret123",
            email="alice@example.com",
            first_name="Alice",
            last_name="Tester",
        )
        today = date.today()
        self.course = Course.objects.create(
            title="English A1",
            start_date=today,
            end_date=today + timedelta(days=30),
        )

    def test_booking_creates_record_and_redirects(self):
        self.client.login(username="alice", password="secret123")

        # GET page ok
        resp_get = self.client.get(reverse("book_tutor"))
        self.assertEqual(resp_get.status_code, 200)

        # Valid POST – includes email so it should succeed
        payload = {
            "name": "Alice Tester",
            "email": "alice@example.com",
            "course": str(self.course.id),
            "message": "Looking forward to it!",
        }
        resp_post = self.client.post(reverse("book_tutor"), data=payload)
        self.assertEqual(resp_post.status_code, 302)
        self.assertEqual(resp_post.headers.get("Location"), reverse("my_bookings"))

        # Booking exists and is linked to user & course
        qs = Booking.objects.filter(user=self.user, course=self.course)
        self.assertTrue(qs.exists(), "Booking record was not created")
        b = qs.first()
        self.assertEqual(b.name, payload["name"])
        self.assertEqual(b.email, payload["email"])

        # My bookings loads
        resp_list = self.client.get(reverse("my_bookings"))
        self.assertEqual(resp_list.status_code, 200)
