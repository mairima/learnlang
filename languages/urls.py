from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.language_list, name='language_list'),
    path('create/', views.language_create, name='language_create'),
    path('<int:pk>/', views.language_detail, name='language_detail'),
    path('<int:pk>/edit/', views.language_update, name='language_update'),
    path('<int:pk>/delete/', views.language_delete, name='language_delete'),
    path('home/', views.home, name='home'),

    # Auth views (these are fine, but make sure templates exist)
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Custom signup view
    path('signup/', views.signup, name='signup'),
]
