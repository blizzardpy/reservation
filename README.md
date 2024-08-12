# Django Time Reservation System

## Project Overview

This project is a time reservation system built using Django, where users can register, log in, and reserve available time slots. The admin can define time slots with specific capacities, and users can book these slots until the capacity is reached.

## Features

- **User Authentication**: Users can register, log in, and log out. Only authenticated users can make reservations.
- **Admin Time Slot Management**: The admin can create, edit, and delete time slots with defined capacities.
- **Real-time Reservation**: Users can select available time slots and make reservations, with the system automatically handling capacity limits.
- **Responsive Design**: The user interface is designed to be responsive and works well on both desktop and mobile devices.

## Prerequisites

Ensure you have the following installed:

- Docker
- Docker Compose

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/DarkSnowJR/reservation
cd reservation
```

### Step 2: Build and Run the Docker Containers

```bash
docker-compose up --build
```

This command will build the Docker image and run the containers for the Django application and the database.

### Step 3: Apply Migrations

Once the containers are up and running, open a new terminal window and apply the migrations:

```bash
docker-compose exec reservation_web python manage.py migrate
```

### Step 4: Create a Superuser

Create an admin user to manage the time slots:

```bash
docker-compose exec reservation_web python manage.py createsuperuser
```

### Step 5: Access the Application

- The application should be running at [http://localhost:8000](http://localhost:8000).
- Access the Django admin panel at [http://localhost:8000/admin](http://localhost:8000/admin) to manage time slots.

## Usage

### Admin:

1. Log in to the admin panel.
2. Create, edit, or delete time slots.
3. Monitor reservations.

### User:

1. Register an account.
2. Log in with your credentials.
3. View available time slots and make a reservation.
4. Receive confirmation of your reservation.

## Running Tests

To run the test suite, use the following command:

```bash
docker-compose exec reservation_web python manage.py test
```

## Troubleshooting

If you encounter any issues, try rebuilding the containers:

```bash
docker-compose down
docker-compose up --build
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, feel free to reach out at great.kian2001@gmail.com.

## Sample ENV Variables

```bash
DJANGO_SECRET_KEY='django-insecure-^=qua!t\*oz5zu1b%acht81ol89x=p4+07tq^q-vq$(bb1=jleo'
DJANGO_DEBUG=True
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=Great.kian2001
POSTGRES_HOST=reservation_db
POSTGRES_PORT=5432
```

---
