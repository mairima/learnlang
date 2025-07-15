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