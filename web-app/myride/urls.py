
from .views import SignUpView

from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView # n ew

from django.http import HttpResponse

from myride import views

urlpatterns = [
    path('registration/',views.registration, name='register'),
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('save/',views.storeInfo,name='storeInfo'),
    path('depart_list/',views.depart_list,name='departList'),
    path('riderequest/',views.riderequest,name='ridereq'),
    path('rideshare/',views.rideshare,name='sharereq'),
    path('settings/',views.dashboard,name='dashboard'),
    path('settings/edit-vehicle/',views.vehicle_edit,name='vehicleEdit'),
    path('settings/edit-user/',views.user_edit,name='userEdit'),
    path('settings/<int:rid>/view-details/',views.ride_view,name='viewRide'),
    path('settings/<int:rid>/edit-ride/',views.ride_edit,name='rideEdit'),
    path('settings/<int:rid>/cancel-ride/',views.ride_cancel,name='rideCancel'),
    path('settings/<int:rid>/select_ride/',views.select_ride),
    path('settings/<int:rid>/cancel_share/',views.share_cancel,name='shareCancel'),
    path('search/', views.search, name='search'),
    path('share_list/', views.shareList, name='share_list'),
    path('share_list/choose_ride/', views.sharechoose, name='choose_ride'),
    path('driver_display/',views.driverDisplay, name='driver_display'),
    path('driver_display/<int:rid>/accept_ride/', views.accept_ride, name='accept_ride'),
    path('driver_display/<int:rid>/complete_ride/', views.complete_ride, name='complete_ride'),




]
