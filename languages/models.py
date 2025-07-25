from django.db import models

# Create your models here.
class Language(models.Model):
    LANGUAGE_CHOICES = [
        ('EN', 'English'),
        ('DE', 'German'),
        ('AR', 'Arabic'),
        ('ZH', 'Chinese'),
    ]

    name = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, unique=True)
    description = models.TextField()
    difficulty = models.CharField(max_length=20)

    def __str__(self):
        return self.get_name_display()
    #CRUD for lessons per language
    # This model can be extended with more fields as needed, such as 'created_at', 'updated_at', etc.

class Category(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # e.g., Vocabulary, Grammar, Phrases
    description = models.TextField(blank=True, null=True)

class Lesson(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
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