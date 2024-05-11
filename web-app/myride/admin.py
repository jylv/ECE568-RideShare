from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import User, Ride, Vehicle, Sharer

admin.site.register(User)

admin.site.register(Ride)
admin.site.register(Vehicle)
admin.site.register(Sharer)

