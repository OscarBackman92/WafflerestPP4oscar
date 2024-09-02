from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page view
    # Add other URL patterns for the home app if needed
]