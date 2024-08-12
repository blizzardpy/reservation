from django.urls import path
from .views import home_view, reserve_view


urlpatterns = [
    path('', home_view, name='home'),
    path('reserve/<int:timeslot_id>', reserve_view, name='reserve'),
]
