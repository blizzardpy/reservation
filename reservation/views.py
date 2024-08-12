from django.contrib import messages
from django.shortcuts import redirect, render
from .models import TimeSlot, Reservation
from datetime import datetime
from django.db import transaction
from django.contrib.auth.decorators import login_required


def home_view(request):
    """
    View function for the home page. It retrieves and filters time slots based on the selected date and user's reservations.

    Parameters:
    request (HttpRequest): The HTTP request object.

    Returns:
    HttpResponse: The rendered home.html template.
    """
    context = {}

    # Check if the user is authenticated
    if request.user.is_authenticated:

        # Get the selected date from the request, default to today's date
        selected_date = request.GET.get(
            'date', datetime.today().strftime('%Y-%m-%d'))

        # Ensure the selected date is not in the past
        if selected_date < datetime.today().strftime('%Y-%m-%d'):
            # If the selected date is in the past, there are no available timeslots
            timeslots = []
        else:
            # Get timeslots for the selected date
            timeslots = TimeSlot.objects.filter(
                date=selected_date, capacity__gt=0)

            # Exclude past timeslots if the selected date is today
            if selected_date == datetime.today().strftime('%Y-%m-%d'):
                timeslots = timeslots.exclude(
                    start_time__lt=datetime.now().time())

            # Handle sorting by start time or end time
            # Default to sorting by start_time
            sort_by = request.GET.get('sort_by', 'start_time')
            sort_order = request.GET.get('sort_order', 'asc')

            # Determine the sorting order
            if sort_order == 'desc':
                sort_by = f'-{sort_by}'

            timeslots = timeslots.order_by(sort_by)

        # Get the user's reserved timeslots
        user_timeslots = TimeSlot.objects.filter(
            reservations__user=request.user)

        # Create the context dictionary to be passed to the template
        context = {
            'timeslots': timeslots,
            'user_timeslots': user_timeslots,
            'selected_date': selected_date,
            'sort_by': sort_by.lstrip('-'),
            'sort_order': sort_order,
        }

    # Render the home.html template with the context
    return render(request, 'home.html', context)


@login_required
def reserve_view(request, timeslot_id):
    """
    View function for reserving a timeslot.

    Args:
        request: HTTP request object.
        timeslot_id: ID of the timeslot to reserve.

    Returns:
        Redirects to the home page if reservation is successful or if the timeslot is already reserved.
        Otherwise, displays an error message.
    """
    # Get the authenticated user
    user = request.user

    # Use transaction.atomic to ensure atomicity of database operations
    with transaction.atomic():
        # Get the timeslot with the given ID
        timeslot = TimeSlot.objects.select_for_update().get(id=timeslot_id)

        # Check if the timeslot is fully booked
        if timeslot.capacity == 0:
            # Display an error message if the timeslot is fully booked
            messages.error(
                request,
                f'Timeslot is fully booked on {timeslot.date} at {timeslot.start_time}')
            return redirect('home')

        # Get or create a reservation for the user and timeslot
        reservation, created = Reservation.objects.select_for_update().get_or_create(
            user=user, timeslot=timeslot)

        # If reservation is created, update the timeslot capacity and save the reservation
        if created:
            timeslot.capacity -= 1
            timeslot.save()
            reservation.save()

            # Display a success message
            messages.success(
                request,
                f'Reservation created successfully for you on {timeslot.date} at {timeslot.start_time}')
            return redirect('home')

        # If reservation already exists, display an error message
        else:
            messages.error(
                request,
                f'Reservation already exists for you on {timeslot.date} at {timeslot.start_time}')
            return redirect('home')
