from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('english/', views.english, name='english'),  # ✅ /english/
    path('english/', views.english_view, name='english'),
    path('get-tutor/', views.get_tutor, name='tutor'),
    path('book/', views.book_tutor, name='booking'),
    path('contact/', views.contact_us, name='contact_us'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('signup/', views.signup, name='signup'),
]