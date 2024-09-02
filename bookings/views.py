from django.shortcuts import render, redirect
from .models import MenuItem, Table, Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required

def make_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookingForm()

    return render(request, 'bookings/make_booking.html', {'form': form})

@login_required
def manage_menu(request):
    # Only admins should be able to manage the menu
    if request.user.is_staff:
        if request.method == 'POST':
            # Handle menu item creation, editing, deletion
            pass
        else:
            menu_items = MenuItem.objects.all()
            return render(request, 'bookings/manage_menu.html', {'menu_items': menu_items})
    else:
        return redirect('home')
