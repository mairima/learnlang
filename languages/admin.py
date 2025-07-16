from django.contrib import admin

# Register your models here.
from .models import Language

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty')
    search_fields = ('name',)