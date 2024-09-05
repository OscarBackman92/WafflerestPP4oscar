from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MenuItem(models.Model):
    """
    A model representing an item on a menu.

    Attributes:
        name (str): The name of the menu item.
        description (str): A detailed description of the menu item.
        price (Decimal): The price of the item, with a maximum of
        6 digits and 2 decimal places.
        category (str): The category of the menu item
        (e.g., Appetizer, Main Course, Dessert).
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50)

    def __str__(self):
        """
        Returns the string representation of the MenuItem, which is the
        name of the item.
        """
        return self.name


class Table(models.Model):
    """
    A model representing a table in the restaurant.

    Attributes:
        size (int): The number of people the table can accommodate.
    """
    size = models.IntegerField()

    def __str__(self):
        """
        Returns the string representation of the Table, showing the
        number of people it can accommodate.
        """
        return f"Table for {self.size} people"


class Booking(models.Model):
    """
    A model representing a booking made by a
    user for a specific table at a given date and time.

    Attributes:
        user (User): The user who made the booking.
        table (Table): The table that is booked.
        date (date): The date of the booking.
        time (time): The time of the booking.
        number_of_guests (int): The number of guests
        for the booking, with a default of 1.

    Meta:
        unique_together: Ensures that a table cannot be
        double-booked for the same date and time.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('table', 'date', 'time')

    def __str__(self):
        """
        Returns the string representation
        of the Booking, showing the table, date, and time.
        """
        return f"Booking for {self.table} on {self.date} at {self.time}"
