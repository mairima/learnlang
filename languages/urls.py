# languages/urls.py
from django.urls import path
from .views import (
    home,
    english,
    get_tutor,
    contact_us,
    book_tutor,
    my_bookings_view,
    edit_booking_view,
    delete_booking_view,
    post_login_redirect,
    student_dashboard,
)

urlpatterns = [
    path("", home, name="home"),

    # Content pages
    path("english/", english, name="english"),
    path("get-tutor/", get_tutor, name="tutor"),  
    path("contact/", contact_us, name="contact_us"),

    # Booking
    path("booking/", book_tutor, name="booking"),
    path("my-bookings/", my_bookings_view, name="my_bookings"),
    path("booking/<int:booking_id>/edit/", edit_booking_view, name="edit_booking"),
    path("booking/<int:booking_id>/delete/", delete_booking_view, name="delete_booking"),

    # Auth routing
    path("after-login/", post_login_redirect, name="after_login"),
    path("dashboard/student/", student_dashboard, name="student_dashboard"),
]
