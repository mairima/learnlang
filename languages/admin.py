from django.contrib import admin
from .models import Lesson, Exercise, Course, Booking


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
