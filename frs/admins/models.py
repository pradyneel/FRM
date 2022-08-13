from django.db import models

# Create your models here.
class Admin(models.Model):
    adminEmail = models.EmailField(max_length=50)
    password = models.CharField(max_length=140)