from django.urls import path
from . import views

urlpatterns = [
    path('', views.language_list, name='language_list'),
    path('create/', views.language_create, name='language_create'),
    path('<int:pk>/', views.language_detail, name='language_detail'),
    path('<int:pk>/edit/', views.language_update, name='language_update'),
    path('<int:pk>/delete/', views.language_delete, name='language_delete'),
]