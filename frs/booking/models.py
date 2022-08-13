from django.db import models
from flights.models import flight
from authenticate.models import User

# Create your models here.
class Booking(models.Model):
    flight_no = models.CharField(max_length=50)
    flight_time = models.TimeField()
    flight_date = models.DateField()
    flight = models.ForeignKey(flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)