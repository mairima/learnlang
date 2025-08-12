from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import time

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
    name = models.CharField(max_length=100)

    # Optional scheduling fields (use if you want real dates / weekend logic)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    weekend_only = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    capacity = models.PositiveIntegerField(default=12)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="bookings")
    name = models.CharField(max_length=100, default="Guest")
    email = models.EmailField(blank=True, null=True)
    date = models.DateField(db_index=True)
    time = models.TimeField(default=time(12, 0))  # Default: 12:00 PM
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # NEW

    class Meta:
        ordering = ("-created_at", "-id")
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], name="uniq_user_course")
        ]

    def __str__(self):
        return f"{self.user} - {self.course} on {self.date} at {self.time}"


# Profile model for user roles
class Profile(models.Model):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("tutor", "Tutor"),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    def __str__(self):
        return f"{self.user.username} ({self.role})"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Automatically ensure a Profile exists for every new User."""
    if created:
        Profile.objects.get_or_create(user=instance)