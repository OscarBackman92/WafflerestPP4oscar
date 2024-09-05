from django import forms
from .models import Booking, Table
from .widgets import TimeSelectWidget
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


class BookingForm(forms.ModelForm):
    """
    A form for creating and validating Booking objects.

    This form handles:
    - Selection of a table, date, time, and number of guests.
    - Validation of table capacity.
    - Prevention of overlapping bookings.
    - Minimum booking duration enforcement.
    - Buffer time enforcement between bookings.
    - Prevention of bookings in the past.
    """

    class Meta:
        model = Booking
        fields = ['table', 'date', 'time', 'number_of_guests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': TimeSelectWidget(),
        }

    def clean(self):
        """
        Perform validation on the cleaned data from the form.

        The following checks are performed:
        1. Prevent bookings in the past.
        2. Ensure the selected table can accommodate the number of guests.
        3. Check for overlapping bookings on the selected table, date, and time
        4. Ensure that bookings last for at least the minimum (1 hour).
        5. Enforce a 30-minute buffer between consecutive bookings.

        Raises:
            ValidationError: If any of the checks fail, Thow ValidationError.
        Returns:
            dict: The cleaned data after passing all validation checks.
        """
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        guests = cleaned_data.get('number_of_guests')
        table = cleaned_data.get('table')

        # Debugging print statements
        print("Form data in clean() method:")
        print(f"date: {date}")
        print(f"time: {time}")
        print(f"guests: {guests}")
        print(f"table: {table}")

        # Get the current date and time
        now = datetime.now()

        # Combine the selected date and time for comparison
        if date and time:
            booking_datetime = datetime.combine(date, time)

            # 0. Check if the booking is in the past
            if booking_datetime < now:
                print("Past booking check failed")
                raise ValidationError("Bookings in the past are not allowed.")

        # 1. Check if the selected table has enough capacity
        if table and table.size < guests:
            print("Capacity check failed")
            raise ValidationError(
                f"The selected table can only accommodate {table.size} guests"
            )

        # 2. Check for overlapping bookings for the selected table
        existing_bookings = Booking.objects.filter(
            table=table, date=date, time=time
        ).exclude(id=self.instance.id)  # Exclude current booking when editing

        if existing_bookings.exists():
            print("Overlapping booking check failed")
            raise ValidationError(
                "The selected table is already booked for this date and time."
            )

        # 3. Check for minimum booking time (e.g., 1 hour)
        MINIMUM_BOOKING_DURATION = timedelta(hours=1)
        booking_end_time = (
            datetime.combine(date, time) + MINIMUM_BOOKING_DURATION
        ).time()

        overlapping_bookings = Booking.objects.filter(
            table=table,
            date=date,
            time__lt=booking_end_time,
            time__gte=time,
        ).exclude(id=self.instance.id)

        if overlapping_bookings.exists():
            print("Minimum booking duration check failed")
            raise ValidationError(
                "The booking duration must be at least 1 hour."
            )

        # 4. Check for buffer time between bookings (e.g., 30 minutes)
        BUFFER_TIME = timedelta(minutes=30)

        # Check for bookings ending within the buffer
        # time before the new booking starts
        bookings_ending_before = Booking.objects.filter(
            table=table,
            date=date,
            time__lte=time,
            time__gte=(datetime.combine(date, time) - BUFFER_TIME).time(),
        ).exclude(id=self.instance.id)

        booking_end_datetime = datetime.combine(date, booking_end_time)
        bookings_starting_after = Booking.objects.filter(
            table=table,
            date=date,
            time__lt=booking_end_time,
            time__gte=(booking_end_datetime - BUFFER_TIME).time(),
        ).exclude(id=self.instance.id)

        if bookings_ending_before.exists() or bookings_starting_after.exists():
            print("Buffer time check failed")
            raise ValidationError(
                "There must be 30min gap between bookings for the same table."
            )

        print("All validation checks passed")
        return cleaned_data
