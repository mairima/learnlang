from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('english/', views.english, name='english'),  # ✅ /english/
    path('english/', views.english_view, name='english'),
    path('get-tutor/', views.get_tutor, name='tutor'),
    path('book/', views.book_tutor, name='booking'),
    path('contact/', views.contact_us, name='contact_us'),
    # crud booking page
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('booking/edit/<int:booking_id>/', views.edit_booking_view, name='edit_booking'),
    path('booking/delete/<int:booking_id>/', views.delete_booking_view, name='delete_booking'),


]