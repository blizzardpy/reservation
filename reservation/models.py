from django.contrib.auth.models import User
from django.db import models


class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.date} {self.start_time} - {self.end_time} (Capacity: {self.capacity})"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation by {self.user.username} for {self.timeslot}"
