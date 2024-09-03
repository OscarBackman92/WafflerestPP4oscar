from django.test import TestCase, Client, override_settings
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from .models import MenuItem, Table, Booking
from .forms import BookingForm
from .utils import send_confirmation_mail
from datetime import datetime, time
import os
from django.conf import settings

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

class UtilsTestCase(TestCase):
    @patch('django.template.loader.render_to_string')
    @patch('bookings.utils.send_mail')
    @override_settings(
        EMAIL_HOST_USER='test@example.com',
        EMAIL_HOST_PASSWORD='testpassword',
    )
    def test_send_confirmation_mail(self, mock_send_mail, mock_render_to_string):
        subject = 'Test Subject'
        recipient_list = ['test@example.com']
        context = {'key': 'value'}
        template_name = 'emails/test_email.html'
        
        # Simulate HTML content rendered from the template
        mock_html_content = '''<!DOCTYPE html>
            <html>
            <head>
                <title>Test Email</title>
            </head>
            <body>
                <p>This is a test email.</p>
                <p>Thank you for using our service.</p>
            </body>
            </html>
        '''
        # Mock the behavior of render_to_string
        mock_render_to_string.return_value = mock_html_content

        # Manually create the plain text content by stripping HTML tags
        breakpoint()
        mock_plain_content = 'This is an HTML version of the email'

        # Call the utility function
        send_confirmation_mail(subject, recipient_list, context, template_name)

        # Verify send_mail is called with the correct parameters
        mock_send_mail.assert_called_once_with(
            subject,
            mock_plain_content,
            settings.EMAIL_HOST_USER,
            recipient_list,
            fail_silently=False,
            html_message=mock_html_content
        )

    def tearDown(self):
        # Reset environment variables after test
        os.environ.pop('EMAIL_HOST_USER', None)
        os.environ.pop('EMAIL_HOST_PASSWORD', None)

