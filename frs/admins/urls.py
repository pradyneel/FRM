from django.urls import path
from .views import *

urlpatterns = [
   path('alogin/', login, name="alogin"),
   path('asignup/', signUp, name="asignup"),
   path('dashboard/', home, name="dashboard"),
   path('alogout/', logout, name="alogout"),
   path('addflight/', addFlight, name="addflight"),
   path('delete/<int:id>', delete, name="delete"),
   path('viewbooks/', viewBookings, name="viewBookings"),
]