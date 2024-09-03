from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Table, Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.html import escape
from .utils import send_confirmation_mail

@login_required
def make_booking(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        
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
                response_data = {'success': False, 'errors': {'__all__': ['No tables available for this date and time.']}}
                if is_ajax:
                    return JsonResponse(response_data)
                else:
                    messages.error(request, 'No tables available for this date and time.')
                    return render(request, 'bookings/make_booking.html', {'form': form})

            # Find the table with the lowest capacity among the available ones
            try:
                lowest_capacity_table = min(available_tables, key=lambda table: table.size)
            except ValueError:
                response_data = {'success': False, 'errors': {'__all__': ['An error occurred while selecting a table. Please try again.']}}
                if is_ajax:
                    return JsonResponse(response_data)
                else:
                    messages.error(request, 'An error occurred while selecting a table. Please try again.')
                    return render(request, 'bookings/make_booking.html', {'form': form})

            booking.table = lowest_capacity_table

            try:
                booking.save()
                
                # Send confirmation email
                context = {
                    'booking': booking,
                    'user': request.user
                }
                send_confirmation_mail(
                    subject='Booking Confirmation',
                    recipient_list=[request.user.email],
                    context=context,
                    template_name='emails/booking_confirmation.html'
                )
                
                response_data = {'success': True, 'message': 'Booking confirmed!'}
                if is_ajax:
                    return JsonResponse(response_data)
                else:
                    messages.success(request, 'Booking confirmed!')
                    return redirect('booking_detail', booking_id=booking.id)
            except Exception as e:
                response_data = {'success': False, 'errors': {'__all__': [f'An error occurred while saving your booking: {escape(str(e))}']}}
                if is_ajax:
                    return JsonResponse(response_data)
                else:
                    messages.error(request, f'An error occurred while saving your booking: {e}')

        # If the form is not valid, re-render the template with the errors
        response_data = {'success': False, 'errors': form.errors.as_json()}
        if is_ajax:
            return JsonResponse(response_data)
        else:
            return render(request, 'bookings/make_booking.html', {'form': form})

    else:  # Handle GET requests (render the form)
        form = BookingForm()

    return render(request, 'bookings/make_booking.html', {'form': form})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def menu(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'bookings/menu.html', {'menu_items': menu_items})

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
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
    
    return render(request, 'bookings/edit_booking.html', {'form': form, 'booking': booking})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
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
        return redirect('my_bookings')  # Redirect to a page that lists bookings or another appropriate page

    return render(request, 'bookings/delete_booking.html', {'booking': booking})

@login_required
def my_bookings(request):
    user = request.user
    bookings = Booking.objects.filter(user=user).order_by('-date', '-time')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})
