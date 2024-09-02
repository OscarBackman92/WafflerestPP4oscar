from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/', views.make_booking, name='make_booking'),
    path('manage-menu/', views.manage_menu, name='manage_menu'),
]
