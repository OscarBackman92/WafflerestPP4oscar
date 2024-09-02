from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Table, Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

@login_required
def make_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('home')
    else:
        form = BookingForm()

    return render(request, 'bookings/make_booking.html', {'form': form})

def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'bookings/menu.html', {'menu_items': menu_items})


