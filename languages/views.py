from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from django.db.models import Count, Q, F, IntegerField, Value
from django.db.models.functions import Greatest

from .models import Booking, Course, Profile
from .forms import BookingForm


# -----------------------------
# Home & simple content pages
# -----------------------------
def home(request):
    return render(request, "home.html")


def english(request):
    """Make this @login_required if you want it private."""
    return render(request, "english.html")


def contact_us(request):
    return render(request, "contact_us.html")


# -----------------------------
# Profile helper
# -----------------------------
def _ensure_profile(user) -> Profile:
    """
    Guarantee the user has a Profile. If missing (e.g., account created before
    the signal existed), create one with a default 'student' role.
    """
    profile, _ = Profile.objects.get_or_create(user=user, defaults={"role": "student"})
    return profile


def login_redirect_by_role(user) -> str:
    _ensure_profile(user)  # keep ensuring profile exists
    return "student_dashboard"


def is_student(user) -> bool:
    if not getattr(user, "is_authenticated", False):
        return False
    return _ensure_profile(user).role == "student"


# -----------------------------
# Post-login router
# -----------------------------
@login_required
def post_login_redirect(request):
    """
    Users land here after login (LOGIN_REDIRECT_URL = 'after_login').
    """
    return redirect(login_redirect_by_role(request.user))


# -----------------------------
# Dashboard (student only)
# -----------------------------
@user_passes_test(is_student)
def student_dashboard(request):
    active_courses = (
        Course.objects
        .annotate(
            booked_count_db=Count(
                "bookings",
                filter=Q(bookings__status__in=["CONFIRMED", "PENDING"]),
                distinct=True,
            )
        )
        .annotate(
            seats_left_db=Greatest(
                F("capacity") - F("booked_count_db"),
                Value(0),
                output_field=IntegerField(),
            )
        )
        .order_by("start_date")
    )
    return render(request, "dashboard/student_dashboard.html", {
        "active_courses": active_courses
    })


# -----------------------------
# Booking: create/list/edit/delete
# -----------------------------
@login_required
def book_tutor(request):
    """
    Booking page (GET shows form; POST creates a booking).
    Uses BookingForm (course, name, email, date, time, message).
    """
    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, "🎉 Booking submitted successfully!")
            return redirect("my_bookings")
        messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm(user=request.user)

    courses = Course.objects.all().order_by("title")
    return render(request, "booking.html", {"form": form, "courses": courses})

@login_required
def get_tutor(request):
    return render(request, "tutor.html")


@login_required
def my_bookings_view(request):
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related("course")
        .order_by("-created_at", "-id")
    )
    return render(request, "my_bookings.html", {"bookings": bookings})


@login_required
def edit_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated.")
            return redirect("my_bookings")
        messages.error(request, "Please fix the errors below.")
    else:
        form = BookingForm(instance=booking, user=request.user)
    return render(request, "edit_booking.html", {"form": form, "booking": booking})


@login_required
def delete_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == "POST":
        booking.delete()
        messages.success(request, "Booking deleted.")
        return redirect("my_bookings")
    return render(request, "delete_booking.html", {"booking": booking})
