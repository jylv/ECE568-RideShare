# accounts/views.py
from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, response
from myride.models import *
from django import forms
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate,login
#from .models import User,Ride




def depart_list(request):
    #check session info of request
    info=request.session.get("info")
    if not info:
        return redirect("/login")
    currUser = User.objects.get(user_id=info)
    #get owned ride
    edit_list = Ride.objects.filter(owner_id=currUser,status=1).all()
    #get shared open ride
    shared = Sharer.objects.filter(sharer_id=currUser.user_id) #share obj
    #edit_list_next = Ride.objects.filter(ride_id=shared)
    #sharer's view only list not yet implemented!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    view_list = Ride.objects.filter(owner_id=currUser,status=2).all()
    completed_list = Ride.objects.filter(owner_id=currUser,status=3).all()
    return render(request, 'depart_list.html',{'owners':edit_list,'shared':shared,'view':view_list,'completed':completed_list})

def home(request):
    return render(request,'home.html')

#-----------------------------driver registration
#model form for registration
class regForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["type","plate_num","max_passenger","special_info"]
        widgets = {
            "type": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter car type"}),
            "plate_num": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter plate number"}),
            "max_passenger": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter maximum passengers"}),
            "special_info": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter any special info you would let others know"})
        }

def registration(request):
    info=request.session.get("info")
    if not info:
        return redirect("/login")
    if request.method=="GET":
        form = regForm()
        return render(request,'registration.html',{"form":form})
    #POST
    form = regForm(data=request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        lastVehicle = Vehicle.objects.last()
        if not lastVehicle:
            obj.vehicle_id = 1
        else:
            obj.vehicle_id = lastVehicle.vehicle_id+1
        currUser = User.objects.get(user_id=info)
        obj.save()
        currUser.vehicle_id = Vehicle.objects.last()
        currUser.save()

        return render(request,'driverRegSuccess.html')
    else:
        return render(request,'registration.html',{"form":form})
#-------------------------------------driver reg end

def storeInfo(request):
    return HttpResponse()

#-----------------------------Sign up
#model form for sign up
class signupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name","user_name","password","email"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter name"}),
            "user_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter user name"}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}),
            "email": forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter your email"})
        }
    def clean(self):
        if self.is_valid():
            cleaned_data = self.cleaned_data
            username = self.cleaned_data['user_name']
            checkUser = User.objects.filter(user_name=username)
            if checkUser:
                raise forms.ValidationError('Username already exists.')
            return cleaned_data

def signup(request):
    if request.method=="GET":
        form = signupForm()
        return render(request,'signup.html',{"form":form})
    #POST
    form = signupForm(data=request.POST)
    if form.is_valid():
        form.clean()
        obj = form.save(commit=False)
        lastUser = User.objects.last()
        if not lastUser:
            obj.user_id = 1
        else:
            obj.user_id = lastUser.user_id+1
        obj.save()
        return redirect("/login")
        #return render(request,'regSuccess.html')
    else:
        return render(request,'signup.html',{"form":form})
#----------------------------------sign up ends

def login(request):
    if request.method=="GET":
        return render(request, "login.html")
    username = request.POST.get("user")
    password = request.POST.get("pwd")
    if User.objects.filter(user_name=username).exists():
        user = User.objects.get(user_name=username)
        if password==user.password:
            response = HttpResponseRedirect('/depart_list')
            # add the user info into session
            request.session["info"]=user.user_id
            return response
        else:
            return render(request, 'login.html', {"err_msg": "Incorrect username or password"})
    else:
        return render(request,'login.html', {"err_msg":"Incorrect username or password"})

def logout(request):
    request.session["info"]=None
    return render(request,'login.html', {"err_msg":"Please login agian"})

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    #return HttpResponse()

def dashboard(request):
    info = request.session.get("info")
    if not info:
        return redirect("/login")
    return render(request,"dashboard.html")

#-----------------------------------need owner id!!!!!!, time stamp need bootstrap
#model form for ride
class rideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ["destination","arrival_date","arrival_time","num_passengers","vehicle_type","special_req"]
        widgets = {
            "destination": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your destination"}),
            "arrival_date": forms.DateInput(attrs={"class": "form-control", "placeholder": "Enter an arrival date. Format: YYYY-MM-DD or MM/DD/YY"}),
            "arrival_time": forms.TimeInput(attrs={"class": "form-control", "placeholder": "Enter an arrival time. Format: HH:MM:SS or HH:MM"}),
            "num_passengers": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter number of passengers"}),
            "vehicle_type": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter a vehicle type that you wish"}),
            "special_req": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter any special info you would let others know"})
        }

def riderequest(request):
    info = request.session.get("info")
    if not info:
        return redirect("/login")
    if request.method=="GET":
        form = rideForm()
        return render(request,'rideRequest.html',{"form":form})
    #POST
    form = rideForm(data=request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        lastRide = Ride.objects.last()
        if not lastRide:
            obj.ride_id = 1
        else:
            obj.ride_id = lastRide.ride_id+1
        #!!!!!!!!!!!!also need owner id
        obj.sharer_num = 0 + obj.num_passengers
        obj.status = 1
        currUser = User.objects.get(user_id=info)
        obj.owner_id = currUser
        obj.save()
        return render(request,'rideRequestSuccess.html')
    else:
        return render(request,'rideRequest.html',{"form":form})


def rideshare(request):
    info = request.session.get("info")
    if not info:
        return redirect("/login")
    if request.method=="GET":
        form = rideForm()
        return render(request,'shareRequest.html',{"form":form})
    #POST
    form = rideForm(data=request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        lastRide = Ride.objects.last()
        if not lastRide:
            obj.ride_id = 1
        else:
            obj.ride_id = lastRide.ride_id+1
        obj.sharer_num = 0
        obj.status = 1
        currUser = User.objects.get(user_id=info)
        obj.owner_id = currUser
        obj.save()
        return render(request,'rideRequestSuccess.html')
    else:
        return render(request,'shareRequest.html',{"form":form})

def search(request ):
    result = request.POST['search']
    if Ride.objects.filter(destination=result).exists():
        ride = Ride.objects.filter(passnum=result).all()
        print(ride.destination,ride.ride_id)
        #form = rideForm(data=request.POST,instance=ride)
        return render(request, 'depart_list.html', {"owners": ride})

def shareList(request):
    allRide = Ride.objects.all()
    return render(request,'share_list.html',{"rides":allRide,"owners":allRide})

def sharechoose(request):
    info = request.session.get("info")
    if not info:
        return redirect("/login")
    dest = request.POST.get('Destination')
    date = request.POST.get('Arrival Date')
    d = datetime.strptime(date,'%b. %d, %Y')
    time = request.POST.get('Arrival Time')
    if time=="noon":
        time="12:00"
    t = datetime.strptime(time,'%H:%M')
    num = request.POST.get('number of passengers')
    allRide = Ride.objects.all()
    ride = Ride.objects.filter(destination=dest, arrival_date__lte=d,arrival_time__lte=t,num_passengers__lte=num).all()
    return render(request, 'share_list.html', {"owners":ride,"rides":allRide})

def driverDisplay(request):
    info = request.session.get("info")
    currUser = User.objects.filter(user_id=info).first()
    vehicle = currUser.vehicle_id
    if not vehicle:
        return redirect('register')
    openRide = Ride.objects.filter(status=1, num_passengers__lte=vehicle.max_passenger, vehicle_type__isnull=True,owner_id__lt=info).all()
    openRide1 = Ride.objects.filter(status=1,num_passengers__lte=vehicle.max_passenger,vehicle_type=vehicle.type,owner_id__lt=info).all()
    type=openRide|openRide1
    Spe = Ride.objects.filter(status=1, num_passengers__lte=vehicle.max_passenger, special_req__isnull=True,owner_id__lt=info).all()
    Spe1 = Ride.objects.filter(status=1, num_passengers__lte=vehicle.max_passenger,special_req=vehicle.special_info,owner_id__lt=info).all()
    specialReq=Spe | Spe1
    rideFinal = type & specialReq

    #status 2 for current driver
    currRide = Ride.objects.filter(driver_id=info,status=2).all()
    return render(request, 'driver_display.html', {"rides":rideFinal,"currs":currRide})

def accept_ride(request,rid):
    info = request.session.get("info")
    if not info:
        return redirect("/login")
    #get current data
    raw_obj = Ride.objects.filter(ride_id=rid).first()
    raw_obj.driver_id = info
    raw_obj.status = 2
    raw_obj.save()
    owner = raw_obj.owner_id
    owner_email = owner.email
    email = EmailMessage('Ride Confirmation', 'This is to confirm that a driver accepted your email', to=[owner_email])
    email.send()
    if raw_obj.num_passengers < raw_obj.sharer_num: #meaning there is at least a sharer
        sharer = Sharer.objects.filter(ride_id=raw_obj).all()
        for sh in sharer:
            sh_id = sh.sharer_id
            currSh = User.objects.get(user_id=sh_id)
            email = EmailMessage('Ride Confirmation', 'This is to confirm that a driver accepted your email', to=[currSh.email])
            email.send()
    return redirect('/driver_display')

def complete_ride(request,rid):
    info = request.session.get("info")
    if not info:
        return redirect("/login")
    ride = Ride.objects.filter(ride_id=rid).first()
    ride.status = 3
    ride.save()
    return redirect('/driver_display')


def vehicle_edit(request):
    info = request.session.get("info")
    if not info:
        return redirect("/login")
    obj = User.objects.get(user_id=info)
    if not obj.vehicle_id:
        return redirect('register')
    if request.method =="GET":
        #get current data
        raw_obj = Vehicle.objects.filter(vehicle_id=obj.vehicle_id.vehicle_id).first()
        form = regForm(instance=raw_obj)
        return render(request,'vehicle_edit.html',{"form":form})
    #POST
    raw_obj = Vehicle.objects.filter(vehicle_id=obj.vehicle_id.vehicle_id).first()
    form = regForm(data=request.POST,instance=raw_obj)
    if form.is_valid():
        form.save()
        return redirect('/settings')
    return render(request, 'vehicle_edit.html', {"form": form})

class editUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name","password","email"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter name"}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}),
            "email": forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter your email"})
        }

def user_edit(request):
    info = request.session.get("info")
    if not info:
        return redirect("/login")
    if request.method =="GET":
        #get current data
        raw_obj = User.objects.filter(user_id=info).first()
        form = editUserForm(instance=raw_obj)
        return render(request,'user_edit.html',{"form":form})
    #POST
    raw_obj = User.objects.filter(user_id=info).first()
    form = editUserForm(data=request.POST,instance=raw_obj)
    if form.is_valid():
        form.save()
        return redirect('/settings')
    return render(request, 'user_edit.html', {"form": form})

def ride_edit(request,rid):
    info = request.session.get("info")
    if not info:
        return redirect("/login")
    if request.method =="GET":
        #get current data
        raw_obj = Ride.objects.filter(ride_id=rid).first()
        form = rideForm(instance=raw_obj)
        return render(request,'ride_edit.html',{"form":form})
    #POST
    raw_obj = Ride.objects.filter(ride_id=rid).first()
    form = rideForm(data=request.POST,instance=raw_obj)
    if form.is_valid():
        form.save()
        return redirect('/depart_list')
    return render(request, 'ride_edit.html', {"form": form})


def ride_view(request,rid):
    info = request.session.get("info")
    if not info:
        return redirect("/login")
    ride = Ride.objects.filter(ride_id=rid).first()
    driver = ride.driver_id
    driver_info = User.objects.filter(user_id=driver).first()
    vehicle_info = driver_info.vehicle_id
    ride.save()
    return render(request,'ride_display.html',{"owner":ride,"driver":driver_info,"vehicle":vehicle_info})

def ride_cancel(request,rid):
    info = request.session.get("info")
    if not info:
        return redirect("/login")
    ride = Ride.objects.get(ride_id=rid)
    ride.delete()
    return redirect('/depart_list')

def share_cancel(request,rid):
    info = request.session.get("info")
    if not info:
        return redirect("/login")
    ride = Ride.objects.get(ride_id=rid)
    share = Sharer.objects.filter(ride_id=ride,sharer_id=info).first()
    ride.sharer_num = ride.sharer_num - share.sharer_num
    ride.save()
    share.delete()
    return redirect('/depart_list')

def select_ride(request,rid):
    info = request.session.get("info")
    if not info:
        return redirect("/login")
    if request.method=="GET":
        return render(request,'select_share.html')
    ride = Ride.objects.get(ride_id=rid)
    if request.method == "POST":
        result = request.POST.get('pass_num')
        ride.sharer_num = ride.sharer_num + int(result)
        share = Sharer(ride_id=ride,sharer_id=info,sharer_num=result)
        ride.save()
        share.save()
    return redirect('/depart_list')


