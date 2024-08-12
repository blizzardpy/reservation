from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .forms import CustomUserCreationForm


def register_view(request):
    """
    Register view handles user registration.

    This view handles both GET and POST requests.
    If the request method is POST, it validates the form data.
    If the form is valid, it saves the user and displays a success message.
    If the form is invalid, it displays an error message.

    Parameters:
    request (HttpRequest): The request object containing metadata about the request.

    Returns:
    HttpResponse: The response containing the rendered HTML template.
    """

    # If the request method is POST, process the form data
    if request.method == 'POST':

        # Create a form instance with the submitted data
        form = CustomUserCreationForm(request.POST)

        # If the form is valid, save the user and display a success message
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')

            # Redirect to login page after successful registration
            return redirect('login')

        # If the form is invalid, display an error message
        else:
            messages.error(request, 'Please correct the errors below.')

    # If the request method is GET, create an empty form
    else:
        form = CustomUserCreationForm()

    # Render the register.html template with the form
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """
    Login view handles user login.

    This view handles both GET and POST requests.
    If the request method is POST, it validates the username and password.
    If the credentials are valid, it logs the user in and redirects to the home page.
    If the credentials are invalid, it displays an error message.

    Parameters:
    request (HttpRequest): The request object containing metadata about the request.

    Returns:
    HttpResponse: The response containing the rendered HTML template.
    """

    # If the request method is POST, process the form data
    if request.method == "POST":
        # Get the username and password from the form
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user with the provided credentials
        user = authenticate(request, username=username, password=password)

        # If the user is authenticated, log them in and redirect to the home page
        if user is not None:
            login(request, user)
            # messages.success(request, 'You have been logged in successfully.')
            return redirect('home')  # Redirect to a success page, e.g., home

        # If the credentials are invalid, display an error message
        else:
            messages.error(request, "Invalid username or password")

    # If the request method is GET, render the login.html template
    return render(request, 'login.html')


def logout_view(request):
    """
    Logout view handles user logout.

    This view logs out the user and redirects them to the home page.
    It also displays a success message indicating that the user has been logged out.

    Parameters:
    request (HttpRequest): The request object containing metadata about the request.

    Returns:
    HttpResponse: The response containing the rendered HTML template.
    """

    # Logout the user
    logout(request)

    # Display a success message indicating that the user has been logged out
    messages.success(request, 'You have been logged out.')

    # Redirect the user to the home page
    return redirect('home')
