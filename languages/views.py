from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.utils import timezone
from django.db.models import Count, Q
from django.views.decorators.http import require_http_methods

from .models import (
    Booking,
    Course,
    Profile,
    ContactMessage,  # noqa: F401 (used via ContactForm save)
)
from .forms import BookingForm, ContactForm


# -----------------------------
# Home & simple content pages
# -----------------------------
def home(request):
    """Public home page."""
    return render(request, "home.html")


def english(request):
    """
    English learning page.
    Add @login_required if you want to restrict to logged-in users only.
    """
    return render(request, "english.html")


def contact_us(request):
    """
    Show the contact form, save submissions to ContactMessage,
    and give user feedback. Admins can view messages in /admin/.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            # Attach logged-in user and backfill name/email if missing
            if request.user.is_authenticated:
                msg.user = request.user
                if not msg.name:
                    msg.name = (
                        request.user.get_full_name()
                        or request.user.username
                    )
                if not msg.email:
                    msg.email = request.user.email or msg.email
            msg.save()
            messages.success(
                request,
                (
                    "Your message has been received. "
                    "An admin will review it shortly."
                ),
            )
            return redirect("contact_us")  # PRG pattern
        messages.error(
            request,
            "Please correct the errors below and resubmit.",
        )
    else:
        # Pre-fill for logged-in users
        initial = {}
        if request.user.is_authenticated:
            initial["name"] = (
                request.user.get_full_name() or request.user.username
            )
            initial["email"] = request.user.email
        form = ContactForm(initial=initial)

    return render(request, "contact_us.html", {"form": form})


# -----------------------------
# Profile helpers
# -----------------------------
def _ensure_profile(user) -> Profile:
    """
    Ensure the user has a Profile.
    If missing, create one with the default role 'student'.
    """
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={"role": "student"},
    )
    return profile


def is_admin(user):
    """
    Check if a user is an admin:
    - Staff or superuser
    - OR profile.role == 'admin'
    """
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
    Redirect users based on role after login:
    - Admin → admin dashboard
    - Others → home
    """
    _ensure_profile(user)  # ensure profile exists
    return "admin_dashboard" if is_admin(user) else "home"


# -----------------------------
# Post-login redirect
# -----------------------------
@login_required
def post_login_redirect(request):
    """Redirect user after login based on their role."""
    list(messages.get_messages(request))  # clear any messages
    return redirect(login_redirect_by_role(request.user))


# -----------------------------
# Dashboard (admin only)
# -----------------------------
@login_required
@user_passes_test(is_admin, login_url="home")
def admin_dashboard(request):
    """
    Admin dashboard showing:
    - Active courses
    - Booked courses
    - Previous bookings
    - Stats
    """
    today = timezone.now().date()

    # Courses that have any booking (all time)
    booked_course_ids = (
        Booking.objects.values_list("course_id", flat=True).distinct()
    )

    # Active = has bookings OR is within date range
    active_filters = (
        Q(id__in=booked_course_ids)
        | Q(start_date__lte=today, end_date__gte=today)
    )

    # Active courses with booking counts
    active_courses = (
        Course.objects.filter(active_filters)
        .annotate(total_bookings=Count("bookings"))
        .distinct()
        .order_by("title")
    )

    # All-time booked courses with counts
    booked_courses = (
        Course.objects.filter(id__in=booked_course_ids)
        .annotate(total_bookings=Count("bookings"))
        .order_by("-id")
    )

    # Last 50 bookings (prefer created_at)
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
    try:
        upcoming_bookings = Booking.objects.filter(
            date__gte=today
        ).count()
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
    Book a tutor:
    - GET → show form with name/email pre-filled if logged in
    - POST → validate (email required) and save booking
    """
    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user)

        # If email is missing, add a field error and re-render (no redirect).
        email_value = (request.POST.get("email") or "").strip()
        if not email_value:
            form.add_error("email", "This field is required.")
            messages.error(request, "Please correct the errors below.")
            courses = Course.objects.all().order_by("title")
            return render(
                request,
                "booking.html",
                {"form": form, "courses": courses},
            )

        # Otherwise validate normally
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(
                request,
                "🎉 Booking submitted successfully!",
            )
            return redirect("my_bookings")

        messages.error(request, "Please correct the errors below.")
    else:
        # Prefill name & email for logged-in users (tests expect name)
        initial = {}
        if request.user.is_authenticated:
            initial["name"] = (
                request.user.get_full_name() or request.user.username
            )
            if getattr(request.user, "email", ""):
                initial["email"] = request.user.email
        form = BookingForm(user=request.user, initial=initial)

    courses = Course.objects.all().order_by("title")
    return render(request, "booking.html", {"form": form, "courses": courses})


@login_required
def get_tutor(request):
    """Page for tutor info (unused if tutors are removed)."""
    return render(request, "tutor.html")


@login_required
def my_bookings_view(request):
    """Show user's bookings."""
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related("course")
        .order_by("-created_at", "-id")
    )
    return render(request, "my_bookings.html", {"bookings": bookings})


@login_required
def edit_booking_view(request, booking_id):
    """Edit a booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == "POST":
        form = BookingForm(
            request.POST, instance=booking, user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated.")
            return redirect("my_bookings")
        messages.error(request, "Please fix the errors below.")
    else:
        form = BookingForm(instance=booking, user=request.user)
    return render(
        request, "edit_booking.html", {"form": form, "booking": booking}
    )


@login_required
def delete_booking_view(request, booking_id):
    """Delete a booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == "POST":
        booking.delete()
        messages.success(request, "Booking deleted.")
        return redirect("my_bookings")
    return render(request, "delete_booking.html", {"booking": booking})


# -----------------------------
# Admin-only password reset
# -----------------------------
@require_http_methods(["GET", "POST"])
def admin_only_password_reset(request):
    """
    Disable allauth's email reset and show admin contact instead.
    """
    if request.method == "POST":
        messages.info(
            request,
            (
                "Password reset is handled by an administrator. "
                "Please contact us for assistance."
            ),
        )
        return redirect("account_login")

    context = {
        "contact_email": "info@learnlang.com",
        "contact_phone": "0049 123456",
    }
    return render(
        request, "account/password_reset_disabled.html", context
    )
