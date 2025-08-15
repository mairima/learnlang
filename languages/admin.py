from django.contrib import admin
from .models import Lesson, Exercise, Course, Booking, ContactMessage
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', )


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'question')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'capacity')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'name', 'status', 'created_at')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
        list_display = ('name', 'email', 'subject', 'created_at')
        search_fields = ('name', 'email', 'subject', 'message')
        list_filter = ('created_at',)
        readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
        ordering = ('-created_at',)
