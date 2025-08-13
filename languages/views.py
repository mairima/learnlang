from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone  # needed for date logic in admin dashboard

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
# Profile helpers
# -----------------------------
def _ensure_profile(user) -> Profile:
    """
    Guarantee the user has a Profile. If missing (e.g., account created before
    the signal existed), create one with a default role (kept as 'student' for compatibility).
    """
    profile, _ = Profile.objects.get_or_create(user=user, defaults={"role": "student"})
    return profile


def is_admin(user):
    """Admin = Django staff/superuser or profile.role == 'admin' (optional)."""
    if not getattr(user, "is_authenticated", False):
        return False
    if user.is_staff or user.is_superuser:
        return True
    try:
        return _ensure_profile(user).role == "admin"
    except Exception:
        return False


def login_redirect_by_role(user) -> str:
    """
    After login:
      - Admins -> admin dashboard
      - Others -> home
    """
    _ensure_profile(user)  # keep ensuring profile exists
    return "admin_dashboard" if is_admin(user) else "home"


# -----------------------------
# Post-login router
# -----------------------------
@login_required
def post_login_redirect(request):
    """
    Users land here after login (LOGIN_REDIRECT_URL = 'post_login_redirect').
    """
    return redirect(login_redirect_by_role(request.user))


# -----------------------------
# Dashboard (admin only)
# -----------------------------
@login_required
@user_passes_test(is_admin, login_url="home")
def admin_dashboard(request):
    """
    Admin-only dashboard.

    Active courses (no 'is_active' field on Course):
      - within date range [start_date, end_date], OR
      - has at least one booking (any time)

    Also shows:
      - courses that ever had a booking (with counts)
      - previous bookings (latest 50)
      - overview stats
    """
    today = timezone.now().date()

    # Courses that have any booking (all time)
    booked_course_ids = Booking.objects.values_list("course_id", flat=True).distinct()

    # Active = has bookings OR is currently within dates
    active_filters = Q(id__in=booked_course_ids) | Q(start_date__lte=today, end_date__gte=today)

    # Use related_name 'bookings' (present in your model according to the error field list)
    active_courses = (
        Course.objects.filter(active_filters)
        .annotate(total_bookings=Count("bookings"))
        .distinct()
        .order_by("title")
    )

    # All-time booked courses (+ counts)
    booked_courses = (
        Course.objects.filter(id__in=booked_course_ids)
        .annotate(total_bookings=Count("bookings"))
        .order_by("-id")
    )

    # Previous bookings (latest first) — prefer created_at; fallback to id if not present
    try:
        previous_bookings = (
            Booking.objects.select_related("course", "user")
            .order_by("-created_at")[:50]
        )
    except Exception:
        previous_bookings = (
            Booking.objects.select_related("course", "user")
            .order_by("-id")[:50]
        )

    # Overview stats
    total_courses = Course.objects.count()
    total_bookings = Booking.objects.count()
    # If your Booking uses a different date field for scheduled time, change 'date' below
    try:
        upcoming_bookings = Booking.objects.filter(date__gte=today).count()
    except Exception:
        upcoming_bookings = None

    context = {
        "today": today,
        "active_courses": active_courses,
        "booked_courses": booked_courses,
        "previous_bookings": previous_bookings,
        "total_courses": total_courses,
        "total_bookings": total_bookings,
        "upcoming_bookings": upcoming_bookings,
    }
    return render(request, "admin_dashboard.html", context)


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
            booking.name = request.user.username
            booking.save()
            messages.success(request, "🎉 Booking submitted successfully!")
            return redirect("my_bookings")
        messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm(
            user=request.user,
            initial={
                "name": request.user.username,
            }
        )

    courses = Course.objects.all().order_by("title")
    return render(request, "booking.html", {"form": form, "courses": courses})


@login_required
def get_tutor(request):
    # If tutors are no longer used, you can safely remove this view and its URL/template.
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
