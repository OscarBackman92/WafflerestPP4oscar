from django.urls import path
from . import views

urlpatterns = [
    path('make_booking/', views.make_booking, name='make_booking'),
    path('menu/', views.menu, name='menu'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
]