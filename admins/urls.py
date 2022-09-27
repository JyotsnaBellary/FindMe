from django.urls import URLPattern, path
from django.contrib import admin
from . import views

urlpatterns = [
    path('adminpage', views.adminpage, name='adminpage'),
    path('adminlogin', views.adminlogin, name='adminlogin'),

]
