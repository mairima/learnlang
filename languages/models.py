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
    class Lesson(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()