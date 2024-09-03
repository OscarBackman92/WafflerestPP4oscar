from datetime import timedelta, date
from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Table, Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse

@login_required
def make_booking(request):
    if request.method == 'POST':
        if request.is_ajax():  # Handle AJAX requests
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.user = request.user

                # Filter tables with sufficient capacity
                tables_with_capacity = Table.objects.filter(size__gte=booking.number_of_guests)

                # Get bookings on the specified date and time
                bookings_on_requested_date_time = Booking.objects.filter(
                    date=booking.date, time=booking.time
                )

                # Exclude tables that are already booked at that time
                available_tables = [
                    table for table in tables_with_capacity 
                    if not any(booking.table == table for booking in bookings_on_requested_date_time)
                ]

                if not available_tables:
                    return JsonResponse({'success': False, 'errors': {'__all__': ['No tables available for this date and time.']}})

                # Find the table with the lowest capacity among the available ones
                lowest_capacity_table = min(available_tables, key=lambda table: table.size)
                booking.table = lowest_capacity_table

                booking.save()
                return JsonResponse({'success': True, 'message': 'Booking confirmed!'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors.as_json()}) 
        else:  # Handle regular form submissions
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.user = request.user

                # Filter tables with sufficient capacity
                tables_with_capacity = Table.objects.filter(size__gte=booking.number_of_guests)

                # Get bookings on the specified date and time
                bookings_on_requested_date_time = Booking.objects.filter(
                    date=booking.date, time=booking.time
                )

                # Exclude tables that are already booked at that time
                available_tables = [
                    table for table in tables_with_capacity 
                    if not any(booking.table == table for booking in bookings_on_requested_date_time)
                ]

                if not available_tables:
                    messages.error(request, 'No tables available for this date and time.')
                    return render(request, 'bookings/make_booking.html', {'form': form})

                # Find the table with the lowest capacity among the available ones
                try:
                    lowest_capacity_table = min(available_tables, key=lambda table: table.size)
                except ValueError: 
                    messages.error(request, 'An error occurred while selecting a table. Please try again.')
                    return render(request, 'bookings/make_booking.html', {'form': form})

                booking.table = lowest_capacity_table

                try:
                    booking.save()
                    messages.success(request, 'Booking confirmed!')
                    return redirect('booking_detail', booking_id=booking.id)
                except Exception as e:
                    messages.error(request, f'An error occurred while saving your booking: {e}')

            # If the form is not valid, re-render the template with the errors
            return render(request, 'bookings/make_booking.html', {'form': form})

    else:  # Handle GET requests (render the form)
        form = BookingForm()

    return render(request, 'bookings/make_booking.html', {'form': form})


def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'bookings/menu.html', {'menu_items': menu_items})

def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})