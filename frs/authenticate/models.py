from django.db import models

# Create your models here.
class User(models.Model):
    userEmail = models.EmailField(max_length=50)
    password = models.CharField(max_length=140)
