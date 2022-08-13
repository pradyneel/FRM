from django.db import models
from authenticate.models import User

# Create your models here.
class flight(models.Model):
    flight_no = models.CharField(max_length=50)
    flight_time = models.TimeField()
    flight_seats = models.CharField(max_length=4)
    flight_date = models.DateField()