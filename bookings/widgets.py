from django import forms
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta


class TimeSelectWidget(forms.Select):
    def __init__(self, *args, **kwargs):
        time_intervals = self.generate_time_intervals()
        kwargs['choices'] = time_intervals
        super().__init__(*args, **kwargs)

    def generate_time_intervals(self):
        intervals = []
        current_time = datetime.strptime('08:00', '%H:%M')
        end_time = datetime.strptime('23:00', '%H:%M')
        while current_time <= end_time:
            intervals.append((
                current_time.strftime('%H:%M'), current_time.strftime('%H:%M')))
            current_time += timedelta(minutes=30)
        return intervals
