from django.urls import path
from . import views

urlpatterns = [
    path('make_booking/', views.make_booking, name='make_booking'),
    path('menu/', views.menu, name='menu'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('edit_booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
]