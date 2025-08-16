from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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

        # GET should render the form with the user's full name in the H
