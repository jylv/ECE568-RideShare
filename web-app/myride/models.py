from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Vehicle(models.Model):
    vehicle_id = models.IntegerField(null=False,primary_key=True)
    type = models.CharField(max_length=20, null=False)
    plate_num = models.CharField(max_length=20, null=False)
    max_passenger = models.IntegerField(null=False)
    special_info = models.CharField(max_length=10, null=True, blank=True)
    '''
    def __str__(self):
        """String for representing the Model object."""
        return self.vehicle_id
    '''

class User(models.Model):
    user_id = models.IntegerField(null=False,primary_key=True)
    name = models.CharField(verbose_name="name",max_length=100,null=False)
    role_choices=(
        (1, "Ride Driver"),
        (2, "Ride Owner"),
        (3, "Ride Sharer"),
    )
    curr_role = models.SmallIntegerField(null=True,choices=role_choices)
    vehicle_id = models.ForeignKey(to="Vehicle", to_field="vehicle_id", on_delete=models.SET_NULL,null=True)
    user_name = models.CharField(verbose_name="user name", max_length=20,null=False)
    password = models.CharField(verbose_name="password", max_length=20,null=False)
    email = models.EmailField(verbose_name="email address", max_length=254, null=False)

'''
    def __str__(self):
        """String for representing the Model object."""
        return self.user_name
'''

class Ride(models.Model):
    ride_id = models.IntegerField(null=False,primary_key=True)
    owner_id = models.ForeignKey(to="User",to_field="user_id", on_delete=models.CASCADE)
    destination = models.CharField(verbose_name="Destination",max_length=100, null=False)
    arrival_date = models.DateField(verbose_name="Arrival Date, format: YYYY-MM-DD or MM/DD/YY")
    arrival_time = models.TimeField(verbose_name="Arrival Time, format: HH:MM:SS or HH:MM")
    num_passengers = models.IntegerField(verbose_name="Number of Passengers", null=False)
    driver_id = models.IntegerField(null=True)
    sharer_num = models.IntegerField(null=True)
    vehicle_type = models.CharField(verbose_name="Car type (optional)", max_length=20,null=True,blank=True)
    status_choices = (
        (1, "not confirmed"),
        (2, "confirmed"),
        (3, "completed"),
    )
    status = models.SmallIntegerField(null=False, choices=status_choices)
    special_req = models.CharField(verbose_name="Special requests (optional)", max_length=100, null=True,blank=True)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('ride-detail', args=[str(self.ride_id)])



class Sharer(models.Model):
    ride_id = models.ForeignKey(to="Ride",to_field="ride_id", on_delete=models.CASCADE)
    sharer_id = models.IntegerField(null=False,primary_key=True)
    sharer_num = models.IntegerField(verbose_name="Number of Sharers", null=False)







