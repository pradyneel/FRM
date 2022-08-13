from django.shortcuts import render, redirect

import booking
from .models import User
from flights.models import flight
from booking.models import Booking
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
#Verify email and Password
def verify_login(email, password):
    user = User.objects.filter(userEmail = email).first()

    #If user doesn't exists
    if user is None:
        return False
    #if user exists
    else:
        password = check_password(password, user.password)
        if password:
            return True
        else:
            return False


def login(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'Login':
            #get login request input
            email = request.POST.get('email')
            password = request.POST.get('password')

            #Verify email and Password
            if verify_login(email, password):
                user = User.objects.filter(userEmail = email).first()
                request.session['user_id'] = user.id
                return redirect('home')

            error = "Incorrect Credentials"
            return render(request, "authenticate/login.html", {"errors": error})
    
    return render(request, 'authenticate/login.html')


def signUp(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'SignUp':
            #Get user Input
            userEmail = request.POST.get('email')
            password = request.POST.get('password')

            #Check if the user already exists
            check_user = User.objects.filter(userEmail = userEmail).first()

            #Return existing user message in SignUp
            if check_user:
                context = {'message': 'User already exists', 'class' : 'danger'}
                return render(request, 'authenticate/signup.html', context)
            else:
                #Hahs password to store in the DB
                password = make_password(password, salt=None, hasher="default")

                #save the user to the DB
                user = User(userEmail = userEmail, password = password)
                user.save()

                #Redirecting user to authenticate/login
                return redirect('login')
    
    return render(request, 'authenticate/signup.html')

#Home Page
def home(request):
    if request.session.get('user_id', None):
        # if request.method == "GET":
        #     #get flights
        #     user_id = request.session['user_id']
        #     time_input = request.GET.get('time') or ''
        #     date_input = request.GET.get('date') or ''

        user_id = request.session['user_id']
        user = User.objects.get(id = user_id)

        context = {
            "user" : user,
        }

        return render(request, "authenticate/home.html", context)
    else:
        context = {'message' : 'Login to View the Home Page', 'class' : 'danger'}
        return redirect('login')

#Logout
def logout(request):
    del request.session['user_id']

    return redirect("login")

#Search
def search(request):
    if request.session.get('user_id', None):
        if request.method == "GET":
            #get flights

            flights = flight.objects.all()
            user_id = request.session['user_id']
            user = User.objects.get(id = user_id)

            context = {
                "flights" : flights,
                "user" : user,
            }
            time_input = request.GET.get('time') or ''
            date_input = request.GET.get('date') or ''

            if time_input and date_input :
                context["flights"] = flight.objects.all().filter(flight_time = time_input, flight_date = date_input)
            return render(request, "authenticate/search.html", context)
    else:
        context = {'message' : 'Login to View the Home Page', 'class' : 'danger'}
        return redirect('login')


#Book
def book(request, flightid, userid):
    if request.session.get('user_id', None):
        flightBook = flight. objects.get(id = flightid)
        userBook = User.objects.get(id = userid)

        if int(flightBook.flight_seats) >= 1:
            flightBook.flight_seats = str(int(flightBook.flight_seats) - 1)
            flightBook.save()

            booking = Booking(flight_no = flightBook.flight_no, flight_time = flightBook.flight_time, flight_date = flightBook.flight_date, flight_id = flightid, user_id = userid)
            booking.save()

        return redirect('search')
    else:
        context = {'message' : 'Login to View the Home Page', 'class' : 'danger'}
        return redirect('login')

#my Booking
def myBooking(request):
    if request.session.get('user_id', None):
        user_id = request.session['user_id']
        booking = Booking.objects.filter(user_id = user_id)

        context = {
            'books' : booking,
        }

        return render(request, "authenticate/mybooking.html", context)
    else:
        context = {'message' : 'Login to View the Home Page', 'class' : 'danger'}
        return redirect('login')