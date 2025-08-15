"""Models for lessons, exercises, courses, bookings, and profiles."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

UserModel = get_user_model()


class Lesson(models.Model):
    """Lesson model."""

    title = models.CharField(max_length=100)
    content = models.TextField()
    description = models.TextField()

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title


class Exercise(models.Model):
    """Exercise linked to a lesson."""

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="exercises",
    )
    question = models.TextField()
    correct_answer = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    explanation = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Exercise for {self.lesson.title}"


class Course(models.Model):
    """A course with capacity and schedule."""

    title = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField(default=10)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ("start_date", "title")

    def __str__(self) -> str:
        return self.title

    @property
    def booked_count(self) -> int:
        """Number of seats currently booked or pending."""
        return self.bookings.filter(
            Q(status="CONFIRMED") | Q(status="PENDING")
        ).count()

    @property
    def seats_left(self) -> int:
        """Remaining available seats (never negative)."""
        return max(self.capacity - self.booked_count, 0)


class Booking(models.Model):
    """A user's booking for a course."""

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    name = models.CharField(max_length=100, default="Guest")
    email = models.EmailField(blank=True, null=True)

    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    class Meta:
        ordering = ("-created_at", "-id")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"],
                name="uniq_user_course",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"{self.user} - {self.course} [{self.status}] • "
            f"{self.created_at:%Y-%m-%d %H:%M}"
        )


class Profile(models.Model):
    """User profile storing the (single) role."""

    ROLE_CHOICES = (("student", "Student"),)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="student",
    )

    def __str__(self) -> str:
        return f"{self.user.username} ({self.role})"


@receiver(post_save, sender=UserModel)
def create_profile(_sender, instance, created, **_kwargs):
    """Ensure every new user has a student profile."""
    if created:
        Profile.objects.get_or_create(
            user=instance,
            defaults={"role": "student"},
        )
