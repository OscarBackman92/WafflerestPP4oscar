from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import MenuItem, Table, Booking
from .forms import BookingForm

class MenuItemModelTest(TestCase):
    def test_menu_item_str(self):
        item = MenuItem.objects.create(name="Pizza", description="Delicious pizza", price=9.99, category="Main Course")
        self.assertEqual(str(item), "Pizza")

class TableModelTest(TestCase):
    def test_table_str(self):
        table = Table.objects.create(size=4)
        self.assertEqual(str(table), "Table for 4 people")

class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.table = Table.objects.create(size=4)

    def test_booking_str(self):
        booking = Booking.objects.create(user=self.user, table=self.table, date="2024-09-03", time="19:00:00", number_of_guests=2)
        self.assertEqual(str(booking), "Booking for Table for 4 people on 2024-09-03 at 19:00:00")

class BookingFormTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(size=4)
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_valid_form(self):
        data = {
            'table': self.table.id,
            'date': '2024-09-03',
            'time': '19:00:00',
            'number_of_guests': 2
        }
        form = BookingForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_due_to_capacity(self):
        table = Table.objects.create(size=2)
        data = {
            'table': table.id,
            'date': '2024-09-03',
            'time': '19:00:00',
            'number_of_guests': 4
        }
        form = BookingForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('The selected table can only accommodate', form.errors['__all__'][0])

    def test_invalid_form_due_to_overlapping_booking(self):
        table = Table.objects.create(size=4)
        Booking.objects.create(user=self.user, table=table, date="2024-09-03", time="19:00:00", number_of_guests=2)

        data = {
            'table': table.id,
            'date': '2024-09-03',
            'time': '19:00:00',
            'number_of_guests': 2
        }
        form = BookingForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('The selected table is already booked for this date and time.', form.errors['__all__'][0])

class MakeBookingViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.table = Table.objects.create(size=4)

    def test_make_booking_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('make_booking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/make_booking.html')

    def test_make_booking_post_valid(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'table': self.table.id,
            'date': '2024-09-03',
            'time': '19:00:00',
            'number_of_guests': 2
        }
        response = self.client.post(reverse('make_booking'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Booking.objects.exists())

    def test_make_booking_post_invalid(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'table': self.table.id,
            'date': '2024-09-03',
            'time': '19:00:00',
            'number_of_guests': 6
        }
        response = self.client.post(reverse('make_booking'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Booking.objects.exists())

