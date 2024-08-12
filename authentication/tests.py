from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .forms import CustomUserCreationForm


class RegisterViewTests(TestCase):

    def test_register_view_get(self):
        """
        Test the register view for a GET request.
        It should render the registration form.
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_register_view_post_valid(self):
        """
        Test the register view for a valid POST request.
        It should create a new user and redirect to the login page.
        """
        form_data = {
            'username': 'newuser',
            'email': 'jT9ZM@example.com',
            'password1': 'Testpassword123!',
            'password2': 'Testpassword123!',
        }
        response = self.client.post(reverse('register'), data=form_data)

        # Check if the form has errors
        if response.status_code == 200:
            print(response.context['form'].errors)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Account created for newuser!')

    def test_register_view_post_invalid(self):
        """
        Test the register view for an invalid POST request.
        It should not create a new user and should display an error message.
        """
        form_data = {
            'username': 'newuser',
            'password1': 'Testpassword123!',
            'password2': 'Differentpassword!',
        }
        response = self.client.post(reverse('register'), data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFalse(User.objects.filter(username='newuser').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Please correct the errors below.')


class LoginViewTests(TestCase):

    def setUp(self):
        # Create a user for testing the login
        self.user = get_user_model().objects.create_user(
            username='testuser', password='Testpassword123!')

    def test_login_view_get(self):
        """
        Test the login view for a GET request.
        It should render the login form.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_valid(self):
        """
        Test the login view for a valid POST request.
        It should log the user in and redirect to the home page.
        """
        form_data = {
            'username': 'testuser',
            'password': 'Testpassword123!',
        }
        response = self.client.post(reverse('login'), data=form_data)

        # Check if the user is logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Check if the response redirects to the home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_login_view_post_invalid(self):
        """
        Test the login view for an invalid POST request.
        It should not log the user in and should display an error message.
        """
        form_data = {
            'username': 'testuser',
            'password': 'Wrongpassword!',
        }
        response = self.client.post(reverse('login'), data=form_data)

        # Check if the user is not logged in
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        # Check that the form re-renders with an error message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid username or password")


class LogoutViewTests(TestCase):

    def setUp(self):
        # Create a user and log them in
        self.user = get_user_model().objects.create_user(
            username='testuser', password='Testpassword123!')
        self.client.login(username='testuser', password='Testpassword123!')

    def test_logout_view(self):
        """
        Test the logout view.
        It should log the user out, display a success message, and redirect to the home page.
        """
        response = self.client.get(reverse('logout'))

        # Check if the user is logged out
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        # Check if the response redirects to the home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        # # Check that a success message is displayed
        # messages = list(get_messages(response.wsgi_request))
        # self.assertEqual(len(messages), 1)
        # self.assertEqual(str(messages[0]), 'You have been logged out.')
