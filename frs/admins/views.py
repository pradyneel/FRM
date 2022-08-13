from django.shortcuts import render, redirect
from .models import Admin
from flights.models import flight
from booking.models import Booking
from django.contrib.auth.hashers import make_password, check_password


"""Admin Login, Logout, Sign Up view Starts"""
#Verify email and Password
def verify_login(email, password):
    admin = Admin.objects.filter(adminEmail = email).first()

    #If admin doesn't exists
    if admin is None:
        return False
    #if admin exists
    else:
        password = check_password(password, admin.password)
        if password:
            return True
        else:
            return False


#Admin Login
def login(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'Login':
            #get login request input
            email = request.POST.get('email')
            password = request.POST.get('password')

            #Verify email and Password
            if verify_login(email, password):
                admin = Admin.objects.filter(adminEmail = email).first()
                request.session['admin_id'] = admin.id
                return redirect('dashboard')

            error = "Incorrect Credentials"
            return render(request, "admins/login.html", {"errors": error})
    
    return render(request, 'admins/login.html')


#Admin Sign Up
def signUp(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'SignUp':
            #Get admin Input
            adminEmail = request.POST.get('email')
            password = request.POST.get('password')

            #Check if the admin already exists
            check_admin = Admin.objects.filter(adminEmail = adminEmail).first()

            #Return existing admin message in SignUp
            if check_admin:
                context = {'message': 'Admin already exists', 'class' : 'danger'}
                return render(request, 'admins/signup.html', context)
            else:
                #Hahs password to store in the DB
                password = make_password(password, salt=None, hasher="default")

                #save the admin to the DB
                admin = Admin(adminEmail = adminEmail, password = password)
                admin.save()

                #Redirecting admin to authenticate/login
                return redirect('alogin')
    
    return render(request, 'admins/signup.html')


#Admin DashBoard
def home(request):
    if request.session.get('admin_id', None):
        admin_id = request.session['admin_id']
        admin = Admin.objects.get(id = admin_id)

        flights = flight.objects.all()

        context = {
            "admin" : admin,
            "flights" : flights,
        }

        return render(request, "admins/home.html", context)
    else:
        context = {'message' : 'Login to View the Home Page', 'class' : 'danger'}
        return redirect('alogin')


#Logout Admin
def logout(request):
    del request.session['admin_id']

    return redirect("alogin")

""""Admin Login, Logout, Sign Up view Ends"""


"""Admin Operations"""
#Add Flight
def addFlight(request):
    if request.session.get('admin_id', None):
        if request.method == "POST":
            admin_id = request.session['admin_id']

            flight_no = request.POST.get('flight_no')
            flight_time = request.POST.get('flight_time')
            flight_seats = request.POST.get('flight_seats')
            flight_date = request.POST.get('flight_date')

            newFlight = flight(flight_no = flight_no, flight_time = flight_time, flight_seats = flight_seats, flight_date = flight_date)
            newFlight.save()
            return redirect('dashboard')
        else:
            admin_id = request.session['admin_id']
            admin = Admin.objects.get(id = admin_id)

            context = {
                "admin" : admin,
            }
            return render(request, "admins/addflight.html", context)
    else:
        context = {'message' : 'Login to View the Home Page', 'class' : 'danger'}
        return redirect('alogin')


#Delete a flight added
def delete(request, id):
    flightDel = flight.objects.get(id = id)
    flightDel.delete()
    
    return redirect('dashboard')


#View Bookings
def viewBookings(request):
    if request.session.get('admin_id', None):
        if request.method == "GET":
            #get booking information

            Bookings = Booking.objects.all()

            context = {
                "books" : Bookings,
            }

            flight_no = request.GET.get('no') or ''
            flight_time = request.GET.get('time') or ''

            print(flight_no)
            print(flight_time)

            if flight_no and flight_time:
                context["books"] = Booking.objects.all().filter(flight_no = flight_no, flight_time = flight_time)
            return render(request, "admins/bookings.html", context)
    else:
        context = {'message' : 'Login to View the Home Page', 'class' : 'danger'}
        return redirect('alogin')
