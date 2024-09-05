from django import forms
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta


class TimeSelectWidget(forms.Select):
    """
    A custom Django form widget for selecting time intervals.

    This widget generates time intervals between 08:00 and 23:00 in 30-minute
    increments and displays them as options in a select dropdown menu.

    Attributes:
        choices: A list of tuples representing the time intervals in the
        format (HH:MM, HH:MM), which is passed to the parent Select widget.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the TimeSelectWidget with time intervals as choices.

        Args:
            *args: Variable length argument list for base widget.
            **kwargs: Arbitrary keyword arguments passed to the base widget.
        """
        time_intervals = self.generate_time_intervals()
        kwargs['choices'] = time_intervals
        super().__init__(*args, **kwargs)

    def generate_time_intervals(self):
        """
        Generates a list of 30-minute time intervals from 08:00 to 23:00.

        Returns:
            A list of tuples where each tuple contains the time in HH:MM format
            for both the value and the display label.
        """
        intervals = []
        current_time = datetime.strptime('08:00', '%H:%M')
        end_time = datetime.strptime('23:00', '%H:%M')
        while current_time <= end_time:
            intervals.append((
                current_time.strftime('%H:%M'),
                current_time.strftime('%H:%M')))
            current_time += timedelta(minutes=30)
        return intervals
