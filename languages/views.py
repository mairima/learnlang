from django.shortcuts import render, redirect, get_object_or_404
from .models import Language
from .forms import LanguageForm
# Import necessary modules for authentication
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

# Import the User model if needed
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_mail('Welcome!', 
                      'Thanks for joining.', 
                      'your_email@gmail.com', 
                      [user.email],
                      fail_silently=True
                      )
            
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def language_list(request):
    languages = Language.objects.all()
    return render(request, 'languages/language_list.html', {'languages': languages})

def language_detail(request, pk):
    language = get_object_or_404(Language, pk=pk)
    return render(request, 'languages/language_detail.html', {'language': language})

def language_create(request):
    form = LanguageForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('language_list')
    return render(request, 'languages/language_form.html', {'form': form})

def language_update(request, pk):
    language = get_object_or_404(Language, pk=pk)
    form = LanguageForm(request.POST or None, instance=language)
    if form.is_valid():
        form.save()
        return redirect('language_list')
    return render(request, 'languages/language_form.html', {'form': form})

def language_delete(request, pk):
    language = get_object_or_404(Language, pk=pk)
    if request.method == "POST":
        language.delete()
        return redirect('language_list')
    return render(request, 'languages/language_confirm_delete.html', {'language': language})
# Home view
def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')

# Login and Logout views
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")