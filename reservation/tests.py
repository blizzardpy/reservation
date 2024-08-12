from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from .models import TimeSlot, Reservation


class HomeViewTests(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = get_user_model().objects.create_user(
            username='testuser', password='Testpassword123!')

        # Create timeslots for testing
        self.timeslot1 = TimeSlot.objects.create(
            date=datetime.today(),
            start_time=(datetime.now() + timedelta(hours=1)).time(),
            end_time=(datetime.now() + timedelta(hours=2)).time(),
            capacity=5
        )
        self.timeslot2 = TimeSlot.objects.create(
            date=datetime.today() + timedelta(days=1),
            start_time=(datetime.now() + timedelta(hours=3)).time(),
            end_time=(datetime.now() + timedelta(hours=4)).time(),
            capacity=3
        )

    def test_home_view_authenticated_user(self):
        """
        Test the home view for an authenticated user.
        It should display timeslots and the user's reservations.
        """
        self.client.login(username='testuser', password='Testpassword123!')

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('timeslots', response.context)
        self.assertIn('user_timeslots', response.context)
        # Only timeslot1 is for today
        self.assertEqual(len(response.context['timeslots']), 1)
        self.assertEqual(response.context['timeslots'][0], self.timeslot1)
        self.assertEqual(
            response.context['selected_date'], datetime.today().strftime('%Y-%m-%d'))

    def test_home_view_unauthenticated_user(self):
        """
        Test the home view for an unauthenticated user.
        It should not display timeslots or user reservations.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertNotIn('timeslots', response.context)
        self.assertNotIn('user_timeslots', response.context)

    def test_home_view_with_sorting(self):
        """
        Test the home view with sorting parameters.
        It should return timeslots sorted by the specified field.
        """
        self.client.login(username='testuser', password='Testpassword123!')

        # Test sorting by end_time in descending order
        response = self.client.get(
            reverse('home'), {'sort_by': 'end_time', 'sort_order': 'desc'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        # Both timeslots should be displayed
        self.assertEqual(len(response.context['timeslots']), 1)
        # timeslot2 should come first in descending order
        self.assertEqual(response.context['timeslots'][0], self.timeslot1)

    def test_home_view_with_selected_date(self):
        """
        Test the home view with a specific selected date.
        It should filter timeslots based on the selected date.
        """
        self.client.login(username='testuser', password='Testpassword123!')

        # Test filtering by tomorrow's date
        selected_date = (datetime.today() + timedelta(days=1)
                         ).strftime('%Y-%m-%d')
        response = self.client.get(reverse('home'), {'date': selected_date})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        # Only timeslot2 should be displayed
        self.assertEqual(len(response.context['timeslots']), 1)
        self.assertEqual(response.context['timeslots'][0], self.timeslot2)
        self.assertEqual(response.context['selected_date'], selected_date)


class ReserveViewTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser', password='Testpassword123!')

        # Create a test timeslot
        self.timeslot = TimeSlot.objects.create(
            date=datetime.today() + timedelta(days=1),
            start_time=(datetime.now() + timedelta(hours=2)).time(),
            end_time=(datetime.now() + timedelta(hours=3)).time(),
            capacity=5
        )

    def test_reserve_view_success(self):
        """
        Test reserving a timeslot successfully.
        """
        self.client.login(username='testuser', password='Testpassword123!')

        response = self.client.post(
            reverse('reserve', args=[self.timeslot.id]))

        # Check if the reservation was created
        self.assertTrue(Reservation.objects.filter(
            user=self.user, timeslot=self.timeslot).exists())

        # Check if the timeslot capacity was decremented
        self.timeslot.refresh_from_db()
        self.assertEqual(self.timeslot.capacity, 4)

        # Check if the response redirects to the home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        # Check that a success message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'Reservation created successfully for you on {
                         self.timeslot.date} at {self.timeslot.start_time}')

    def test_reserve_view_fully_booked(self):
        """
        Test attempting to reserve a fully booked timeslot.
        """
        self.client.login(username='testuser', password='Testpassword123!')

        # Set the timeslot capacity to 0 to simulate fully booked
        self.timeslot.capacity = 0
        self.timeslot.save()

        response = self.client.post(
            reverse('reserve', args=[self.timeslot.id]))

        # Check that no reservation was created
        self.assertFalse(Reservation.objects.filter(
            user=self.user, timeslot=self.timeslot).exists())

        # Check if the response redirects to the home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        # Check that an error message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), f'Timeslot is fully booked on {self.timeslot.date.strftime("%Y-%m-%d")} at {self.timeslot.start_time}')

    def test_reserve_view_already_reserved(self):
        """
        Test attempting to reserve a timeslot that the user has already reserved.
        """
        self.client.login(username='testuser', password='Testpassword123!')

        # Create a reservation for the user
        Reservation.objects.create(user=self.user, timeslot=self.timeslot)

        response = self.client.post(
            reverse('reserve', args=[self.timeslot.id]))

        # Check that no additional reservation was created
        self.assertEqual(Reservation.objects.filter(
            user=self.user, timeslot=self.timeslot).count(), 1)

        # Check if the response redirects to the home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        # Check that an error message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), f'Reservation already exists for you on {self.timeslot.date.strftime("%Y-%m-%d")} at {self.timeslot.start_time}')
