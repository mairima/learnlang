from django.db import models
from django.contrib.auth.models import User

# Create your models here.

    #CRUD for lessons per language
    # This model can be extended with more fields as needed, such as 'created_at', 'updated_at', etc.
class Lesson(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    description = models.TextField()
    audio = models.FileField(upload_to='audios/', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
        
    def __str__(self):
        return self.title

class Exercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question = models.TextField()
    correct_answer = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    explanation = models.TextField(blank=True)