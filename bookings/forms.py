from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from .models import Booking, Table

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['table', 'date', 'time', 'number_of_guests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        guests = cleaned_data.get('number_of_guests')
        table = cleaned_data.get('table')

        print("Form data in clean() method:")
        print("date:", date)
        print("time:", time)
        print("guests:", guests)
        print("table:", table)

        # 1. Check if the selected table has enough capacity
        if table and table.size < guests:
            print("Capacity check failed")
            raise ValidationError(f"The selected table can only accommodate {table.size} guests.")

        # 2. Check for overlapping bookings for the selected table
        existing_bookings = Booking.objects.filter(table=table, date=date, time=time)
        if existing_bookings.exists():
            print("Overlapping booking check failed")
            raise ValidationError("The selected table is already booked for this date and time.")

        # 3. Check for minimum booking time (e.g., 1 hour)
        MINIMUM_BOOKING_DURATION = timedelta(hours=1) 
        booking_end_time = (datetime.combine(date, time) + MINIMUM_BOOKING_DURATION).time()

        overlapping_bookings = Booking.objects.filter(
            table=table,
            date=date,
            time__lt=booking_end_time, 
            time__gte=time, 
        )
        if overlapping_bookings.exists():
            print("Minimum booking duration check failed")
            raise ValidationError("The booking duration must be at least 1 hour.")

        # 4. Check for buffer time between bookings (e.g., 30 minutes)
        BUFFER_TIME = timedelta(minutes=30)

        # Check for bookings ending within the buffer time before the new booking starts
        bookings_ending_before = Booking.objects.filter(
            table=table,
            date=date,
            time__lte=time,
            time__gte=(datetime.combine(date, time) - BUFFER_TIME).time(),
        )

        # CORRECTED LINE: Combine time with date before subtraction
        booking_end_datetime = datetime.combine(date, booking_end_time)
        bookings_starting_after = Booking.objects.filter(
            table=table,
            date=date,
            time__lt=booking_end_time,
            time__gte=(booking_end_datetime - BUFFER_TIME).time(),  
        )

        if bookings_ending_before.exists() or bookings_starting_after.exists():
            print("Buffer time check failed")
            raise ValidationError("There must be a 30-minute buffer between bookings on the same table.")

        print("All validation checks passed")
        return cleaned_data
