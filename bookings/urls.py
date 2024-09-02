from django.urls import path
from . import views

urlpatterns = [
    path('make_booking/', views.make_booking, name='make_booking'),
    path('manage_menu/', views.manage_menu, name='manage_menu'),
    # Add other URL patterns here
]