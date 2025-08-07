from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail

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
def english(request):
    return render(request, 'english.html')
# english view2
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

