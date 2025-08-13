# languages/urls.py
from django.urls import path
from .import views # import views

urlpatterns = [
    path("", views.home, name="home"), 

    # Content pages
    path("english/", views.english, name="english"),
    path("get-tutor/", views.get_tutor, name="tutor"),
    path("contact/", views.contact_us, name="contact_us"),

    # Booking
    path("booking/", views.book_tutor, name="booking"),
    path("my-bookings/", views.my_bookings_view, name="my_bookings"),
    path("booking/<int:booking_id>/edit/", views.edit_booking_view, name="edit_booking"),
    path("booking/<int:booking_id>/delete/", views.delete_booking_view, name="delete_booking"),

    # Auth routing
    path("after-login/", views.post_login_redirect, name="after_login"),
    path("", views.home, name="home"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    # Admin dashboard only
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
]
