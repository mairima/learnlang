from datetime import time as time_obj

from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


# Lessons
class Lesson(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    description = models.TextField()

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title


# Exercises linked to a lesson
class Exercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="exercises")
    question = models.TextField()
    correct_answer = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"Exercise for {self.lesson.title}"


class Course(models.Model):
    title = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField(default=10)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ("start_date", "title")

    def __str__(self):
        return self.title

    @property
    def booked_count(self):
        # Count only active/confirmed seats
        return self.bookings.filter(Q(status="CONFIRMED") | Q(status="PENDING")).count()

    @property
    def seats_left(self):
        return max(self.capacity - self.booked_count, 0)


class Booking(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="bookings")

    name = models.CharField(max_length=100, default="Guest")
    email = models.EmailField(blank=True, null=True)

    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    class Meta:
        ordering = ("-created_at", "-id")
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], name="uniq_user_course"),
        ]

    def __str__(self):
        return f"{self.user} - {self.course} on {self.date} at {self.time}"


# Profile model for user roles (now student-only)
class Profile(models.Model):
    # Single role left to avoid removing the column everywhere
    ROLE_CHOICES = (("student", "Student"),)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    def __str__(self):
        return f"{self.user.username} ({self.role})"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Ensure every new user has a student profile."""
    if created:
        Profile.objects.get_or_create(user=instance, defaults={"role": "student"})
