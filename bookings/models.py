from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Table(models.Model):
    size = models.IntegerField()

    def __str__(self):
        return f"Table for {self.size} people"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField(default=1)


    class Meta:
        unique_together = ('table', 'date', 'time')

    def __str__(self):
        return f"Booking for {self.table} on {self.date} at {self.time}"