from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from languages.models import Course

User = get_user_model()


class FunctionalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="pw123456",
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
        )
        today = date.today()
        self.course = Course.objects.create(
            title="English A1",
            start_date=today,
            end_date=today + timedelta(days=30),
        )

    def test_booking_prefills_name_and_requires_email(self):
        """
        - GET /book/ pre-fills user's name (verify in HTML)
        - POST without email re-renders with error text (verify in HTML)
        """
        self.client.login(username="testuser", password="pw123456")

        # 1) GET should render the form with the user's full name present in the HTML
        resp_get = self.client.get(reverse("book_tutor"))
        self.assertEqual(resp_get.status_code, 200)
        expected_name = f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
        # Look for the name value somewhere in the rendered page (e.g., input value or text)
        self.assertContains(resp_get, expected_name)

        # 2) POST without email -> expect 200 (no redirect) and the error text in the HTML
        payload = {
            "name": expected_name,
            "email": "",  # trigger required error
            "course": str(self.course.id),
            "message": "Hi!",
        }
        resp_post = self.client.post(reverse("book_tutor"), data=payload)
        self.assertEqual(resp_post.status_code, 200)
        # Default Django form error text for required fields
        self.assertContains(resp_post, "This field is required.")
