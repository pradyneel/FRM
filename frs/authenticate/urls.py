from django.urls import path
from .views import *

urlpatterns = [
    path('', login, name="login"),
    path('signup/', signUp, name="signup"),
    path('home/', home, name="home"),
    path('logout/', logout, name="logout"),
    path('search/', search, name="search"),
    path('book/<int:flightid>/<int:userid>', book, name="book"),
    path('mybooking/', myBooking, name="myBooking"),
]
