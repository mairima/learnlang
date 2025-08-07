from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
#Add bookingpage crud
from .models import Booking, Course
from .forms import BookingForm

# --- New Signup View ---
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

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
def book_tutor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        message = request.POST.get('message')

        # Save the booking (adjust model name/fields as needed)
        Booking.objects.create(
            name=name,
            email=email,
            date=date,
            time=time,
            message=message,
            user=request.user  # if your Booking model has a user ForeignKey
        )

        messages.success(request, 'Booking submitted successfully!')
        return redirect('my_bookings')  # or redirect to another page

    return render(request, 'booking_form.html')