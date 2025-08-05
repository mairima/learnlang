from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('languages/', views.language_list, name='language_list'),  # ✅ /languages/

    path('english/', views.english, name='english'),  # ✅ /english/
    path('get-tutor/', views.get_tutor, name='tutor'),
path('book/', views.book_tutor, name='booking'),

    # Language CRUD
    path('languages/create/', views.language_create, name='language_create'),
    path('languages/<int:pk>/edit/', views.language_update, name='language_update'),
    path('languages/<int:pk>/delete/', views.language_delete, name='language_delete'),
    path('languages/<int:pk>/', views.language_detail, name='language_detail'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('signup/', views.signup, name='signup'),
]