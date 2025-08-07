from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
#Add bookingpage crud
from .models import Booking, Course
from .forms import BookingForm



# Home view
def home(request):
    return render(request, 'home.html')
# English view
def english_view(request):
    return render(request, 'english.html')
def get_tutor(request):
    return render(request, 'tutor.html')

def book_tutor(request):
    return render(request, 'booking.html')
def contact_us(request):
    return render(request, 'contact_us.html')

#Restricted view-Booking page
@login_required
def book_tutor(request):
    return render(request, 'booking.html')
#restricted view-english page
@login_required
def english(request):
    return render(request, 'english.html')

# Crud Booking page
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def edit_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('my_bookings')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'edit_booking.html', {'form': form})

@login_required
def delete_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        return redirect('my_bookings')
    return render(request, 'delete_booking.html', {'booking': booking})

# Message for booking confirmation
@login_required
def book_tutor(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = Course.objects.get(id=course_id)

        Booking.objects.create(
            user=request.user,
            course=course,
            name=request.POST['name'],
            email=request.POST.get('email'),
            date=request.POST['date'],
            time=request.POST['time'],
            message=request.POST.get('message'),
        )
        messages.success(request, '🎉 Booking submitted successfully!')
        return redirect('my_bookings')  # or stay on same page if needed

    courses = Course.objects.all()
    return render(request, 'booking.html', {'courses': courses})
# Login required for my bookings
@login_required()  # This redirects to /login if not logged in
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})