from django.db import models
from django.contrib.auth.models import User
import datetime

# Crud for lessons
class Lesson(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    description = models.TextField()
    audio = models.FileField(upload_to='audios/', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title

# Crud for exercises linked to a lesson
class Exercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question = models.TextField()
    correct_answer = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    explanation = models.TextField(blank=True)

class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Guest")
    email = models.EmailField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField(default=datetime.time(12, 0))  # Default: 12:00 PM
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.name} on {self.date} at {self.time}"