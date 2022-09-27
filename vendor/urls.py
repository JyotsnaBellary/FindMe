from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from findme.settings import STATIC_URL, STATICFILES_DIRS
from .import views
from .views import * 

urlpatterns = [
    path('vendor', views.vendor, name="vendor"),
    path('order', views.order, name="order"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('vendor_profile', views.vendor_profile, name="vendor_profile"),
    path('notverified', views.notverified, name="notverified"),
    path('change_status/<status>/<order_id>/<product_id>', views.change_status, name="change_status" ),
    path('bussiness_profile', views.bussiness_profile, name="bussiness_profile" ),
    path('add_products', views.add_products, name="add_products"),
    path('delete_products/<product>', views.delete_products, name="delete_products"),

] 

