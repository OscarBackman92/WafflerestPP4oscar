from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Table, Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import send_confirmation_mail
from django.core.exceptions import PermissionDenied


@login_required
def make_booking(request):
    """
    Handle the process of making a new booking.

    If the request method is POST, the booking
    form is validated and a table is selected
    based on the number of guests and availability
    If valid, the booking is saved,
    a confirmation email is sent,
    and the user is redirected to the booking detail page.
    Otherwise, the form is re-rendered with error messages.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered booking creation page
        or a redirect to the booking detail.
    """
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
                    request, 'An error occurred while selecting a table.')
                return render(
                    request, 'bookings/make_booking.html', {'form': form})

            booking.table = lowest_capacity_table

            try:
                booking.save()

                # Prepare email context
                context = {'booking': booking, 'user': request.user}

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
                    request, f'An error occurred when saving your booking {e}')

        return render(request, 'bookings/make_booking.html', {'form': form})

    else:
        form = BookingForm()

    return render(request, 'bookings/make_booking.html', {'form': form})


@login_required
def delete_booking(request, booking_id):
    """
    Handle the deletion of a booking by the user.

    If the request method is POST, the
    booking is deleted, a cancellation email is sent,
    and the user is redirected to their
    bookings page. If the booking doesn't belong
    to the user, a permission denied exception is raised.

    Args:
        request: The HTTP request object.
        booking_id: The ID of the booking to delete.

    Returns:
        HttpResponse: The rendered delete
        confirmation page or a redirect to the user's bookings.
    """
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        try:
            booking.delete()

            # Prepare email context
            context = {'booking': booking, 'user': request.user}

            # Send cancellation email
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
                request, f'An error occurred while deleting your booking: {e}')

    return render(
        request, 'bookings/delete_booking.html', {'booking': booking})


@login_required
def booking_detail(request, booking_id):
    """
    Display the details of a specific booking.

    If the booking doesn't belong to the
    logged-in user, a permission denied exception is raised.

    Args:
        request: The HTTP request object.
        booking_id: The ID of the booking to view.

    Returns:
        HttpResponse: The rendered booking detail page.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user != request.user:
        raise PermissionDenied()
    return render(
        request, 'bookings/booking_detail.html', {'booking': booking})


def menu(request):
    """
    Display the restaurant's menu items.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered menu page with a list of all menu items.
    """
    menu_items = MenuItem.objects.all()
    return render(request, 'bookings/menu.html', {'menu_items': menu_items})


@login_required
def edit_booking(request, booking_id):
    """
    Handle the editing of an existing booking.

    If the booking belongs to the user,
    the form is displayed for editing. On POST, the updated
    booking is saved and a confirmation email
    is sent. If the booking doesn't belong to the user,
    a permission denied exception is raised.

    Args:
        request: The HTTP request object.
        booking_id: The ID of the booking to edit.

    Returns:
        HttpResponse: The rendered edit booking page
        or a redirect to the booking detail page.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user == request.user:
        if request.method == 'POST':
            form = BookingForm(request.POST, instance=booking)
            if form.is_valid():
                form.save()

                # Send confirmation email
                context = {'booking': booking, 'user': request.user}
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
def my_bookings(request):
    """
    Display a list of all bookings made
    by the logged-in user, ordered by date and time.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered page showing the user's bookings.
    """
    user = request.user
    bookings = Booking.objects.filter(user=user).order_by('-date', '-time')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})
