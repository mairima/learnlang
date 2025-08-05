from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail

from .models import Language
from .forms import LanguageForm

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


# --- Language Views ---
def language_list(request):
    languages = Language.objects.all()
    return render(request, 'languages/language_list.html', {'languages': languages})

def language_detail(request, pk):
    language = get_object_or_404(Language, pk=pk)
    return render(request, 'languages/language_detail.html', {'language': language})

@login_required
def language_create(request):
    if not request.user.is_superuser:
        messages.error(request, "You must be an admin to perform this action.")
        return redirect('language_list')

    form = LanguageForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('language_list')
    return render(request, 'languages/language_form.html', {'form': form})

@login_required
def language_update(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You must be an admin to perform this action.")
        return redirect('language_list')
    language = get_object_or_404(Language, pk=pk)
    form = LanguageForm(request.POST or None, instance=language)
    if form.is_valid():
        form.save()
        return redirect('language_list')
    return render(request, 'languages/language_form.html', {'form': form})

@login_required
def language_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "You must be an admin to perform this action.")
        return redirect('language_list')
    language = get_object_or_404(Language, pk=pk)
    if request.method == "POST":
        language.delete()
        return redirect('language_list')
    return render(request, 'languages/language_confirm_delete.html', {'language': language})


# Home view
def home(request):
    return render(request, 'home.html')
# English view
def english(request):
    return render(request, 'english.html')
