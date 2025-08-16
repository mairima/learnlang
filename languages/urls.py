# languages/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("english/", views.english, name="english"),
    path("contact/", views.contact_us, name="contact_us"),

    # Booking
    path("book/", views.book_tutor, name="book_tutor"),
    path("book/", views.book_tutor, name="booking"),  # alias
    path("tutor/", views.get_tutor, name="get_tutor"),
    path("tutor/", views.get_tutor, name="tutor"),  # alias
    path("my-bookings/", views.my_bookings_view, name="my_bookings"),
    path(
        "bookings/<int:booking_id>/edit/",
        views.edit_booking_view,
        name="edit_booking",
    ),
    path(
        "bookings/<int:booking_id>/delete/",
        views.delete_booking_view,
        name="delete_booking",
    ),

    # Post-login & admin
    path("after-login/", views.post_login_redirect, name="after_login"),
    path(  # alias
        "after-login/",
        views.post_login_redirect,
        name="post_login_redirect",
    ),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path(  # alias
        "admin-dashboard/",
        views.admin_dashboard,
        name="tutor_dashboard",
    ),
    path(  # alias
        "admin-dashboard/",
        views.admin_dashboard,
        name="student_dashboard",
    ),

    # Password reset placeholder
    path(
        "account/password/reset/",
        views.admin_only_password_reset,
        name="account_reset_password",
    ),
]
