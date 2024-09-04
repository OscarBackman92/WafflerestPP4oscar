from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import MenuItem, Table, Booking
from .forms import BookingForm
from django.core.exceptions import PermissionDenied



class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.table = Table.objects.create(size=4)
        self.booking = Booking.objects.create(
            user=self.user,
            table=self.table,
            date='2024-09-10',
            time='18:00',
            number_of_guests=2
        )

    def test_make_booking_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('make_booking'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/make_booking.html')
        self.assertIsInstance(response.context['form'], BookingForm)

    def test_make_booking_post_success(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'date': '2024-09-15',
            'time': '19:00',
            'number_of_guests': 2
        }
        response = self.client.post(reverse('make_booking'), data)

    def test_make_booking_post_no_tables(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'date': '2024-09-10',
            'time': '18:00',
            'number_of_guests': 2
        }
        response = self.client.post(reverse('make_booking'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/make_booking.html')
        messages_list = list(response.context['messages'])
        

    def test_delete_booking_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('delete_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/delete_booking.html')

    def test_delete_booking_post_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_booking', args=[self.booking.id]))
        self.assertRedirects(response, reverse('my_bookings'))
        self.assertEqual(len(Booking.objects.all()), 0)

    def test_delete_booking_post_wrong_user(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')
        response = self.client.post(reverse('delete_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 403)

    def test_booking_detail(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('booking_detail', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_detail.html')

    def test_booking_detail_wrong_user(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')

    def test_menu(self):
        MenuItem.objects.create(name='Pizza', price=10.99, description='Delicious pizza')
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/menu.html')
        self.assertEqual(len(response.context['menu_items']), 1)

    def test_edit_booking_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('edit_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/edit_booking.html')
        self.assertIsInstance(response.context['form'], BookingForm)

    def test_edit_booking_post_success(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'date': '2024-09-20',
            'time': '20:00',
            'number_of_guests': 3
        }
        response = self.client.post(reverse('edit_booking', args=[self.booking.id]), data)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.number_of_guests, 2)

    def test_edit_booking_wrong_user(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')


    def test_my_bookings(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/my_bookings.html')
        self.assertEqual(len(response.context['bookings']), 1)