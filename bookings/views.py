from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Table, Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import send_confirmation_mail
from django.core.exceptions import PermissionDenied


@login_required
def make_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user

            # Filter tables with sufficient capacity
            tables_with_capacity = Table.objects.filter(
                size__gte=booking.number_of_guests)

            # Get bookings on the specified date and time
            bookings_on_requested_date_time = Booking.objects.filter(
                date=booking.date, time=booking.time
            )

            # Exclude tables that are already booked at that time
            available_tables = [
                table for table in tables_with_capacity
                if not any(
                    existing_booking.table == table for
                    existing_booking in bookings_on_requested_date_time)
            ]

            if not available_tables:
                messages.error(
                    request, 'No tables available for this date and time.')
                return render(
                    request, 'bookings/make_booking.html', {'form': form})

            # Find the table with the lowest capacity among the available ones
            try:
                lowest_capacity_table = min(
                    available_tables, key=lambda table: table.size)
            except ValueError:
                messages.error(
                    request,
                    'An error occurred while selecting a table. Please fix')
                return render(
                        request, 'bookings/make_booking.html', {'form': form})

            booking.table = lowest_capacity_table

            try:
                booking.save()

                # Prepare email context
                context = {
                    'booking': booking,
                    'user': request.user
                }

                # Send confirmation email
                send_confirmation_mail(
                    subject='Booking Confirmation',
                    recipient_list=[request.user.email],
                    context=context,
                    template_name='emails/booking_confirmation.html'
                )

                messages.success(request, 'Booking confirmed!')
                return redirect('booking_detail', booking_id=booking.id)

            except Exception as e:
                messages.error(
                    request,
                    f'An error occurred while saving your booking: {e}')

        # If the form is not valid, re-render the template with the errors
        return render(request, 'bookings/make_booking.html', {'form': form})

    else:
        form = BookingForm()

    return render(request, 'bookings/make_booking.html', {'form': form})


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        try:
            booking.delete()

            # Prepare email context
            context = {
                'booking': booking,
                'user': request.user
            }

            # Send confirmation email
            send_confirmation_mail(
                subject='Booking Cancelled',
                recipient_list=[request.user.email],
                context=context,
                template_name='emails/booking_cancellation.html'
            )

            messages.success(request, 'Booking deleted successfully.')
            return redirect('my_bookings')
        except Exception as e:
            messages.error(
                request,
                f'An error occurred while deleting your booking: {e}'
            )

    return render(
        request, 'bookings/delete_booking.html', {'booking': booking})


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user != request.user:
        raise PermissionDenied()
    return render(
        request, 'bookings/booking_detail.html', {'booking': booking})


def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'bookings/menu.html', {'menu_items': menu_items})


@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user == request.user:

        if request.method == 'POST':
            form = BookingForm(request.POST, instance=booking)
            if form.is_valid():
                form.save()

                # Send confirmation email
                context = {
                    'booking': booking,
                    'user': request.user
                }
                send_confirmation_mail(
                    subject='Booking Updated',
                    recipient_list=[request.user.email],
                    context=context,
                    template_name='emails/booking_update.html'
                )

                messages.success(request, 'Booking updated!')
                return redirect('booking_detail', booking_id=booking.id)
        else:
            form = BookingForm(instance=booking)
    else:
        raise PermissionDenied()
    return render(
        request,
        'bookings/edit_booking.html', {'form': form, 'booking': booking})


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user == request.user:

        if request.method == 'POST':
            booking.delete()

            # Send confirmation email
            context = {
                'booking': booking,
                'user': request.user
            }
            send_confirmation_mail(
                subject='Booking Cancelled',
                recipient_list=[request.user.email],
                context=context,
                template_name='emails/booking_cancellation.html'
            )

            messages.success(request, 'Booking deleted successfully.')
            return redirect('my_bookings')

    else:
        raise PermissionDenied()
    return render(
        request, 'bookings/delete_booking.html', {'booking': booking})
    user = request.user


@login_required
def my_bookings(request):
    user = request.user
    bookings = Booking.objects.filter(user=user).order_by('-date', '-time')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})
