import numbers
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
import uuid

from vendor.models import *
# Create your models here.

# def filepath():


class register(models.Model):
    # class for customers
    user_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    name = models.CharField(max_length=26, blank=True)
    username = models.CharField(max_length=26, blank=True)
    email = models.CharField(max_length=26, blank=True)
    password = models.CharField(max_length=220, blank=True)
    # aggreement = models.CharField(max_length=20)
    
    class Meta:
        unique_together = (("username", "email"),)
        def __str__(self):
            return self.user_id

# class MyAccountManager(BaseUserManager):
#     def create_user(self, first_name, last_name, username, email, password=None):
#         if not email:
#             raise ValueError('User must have an email address')

#         if not username:
#             raise ValueError('User must have an username')

#         user = self.model(
#             email = self.normalize_email(email),
#             username = username,
#             first_name = first_name,
#             last_name = last_name,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, first_name, last_name, email, username, password):
#         user = self.create_user(
#             email = self.normalize_email(email),
#             username = username,
#             password = password,
#             first_name = first_name,
#             last_name = last_name,
#         )
#         user.is_admin = True
#         user.is_active = True
#         user.is_staff = True
#         user.is_superadmin = True
#         user.save(using=self._db)
#         return user



# class Account(AbstractBaseUser):
#     first_name      = models.CharField(max_length=50)
#     last_name       = models.CharField(max_length=50)
#     username        = models.CharField(max_length=50, unique=True)
#     email           = models.EmailField(max_length=100, unique=True)
#     phone_number    = models.CharField(max_length=50)

#     # required
#     date_joined     = models.DateTimeField(auto_now_add=True)
#     last_login      = models.DateTimeField(auto_now_add=True)
#     is_admin        = models.BooleanField(default=False)
#     is_staff        = models.BooleanField(default=False)
#     is_active        = models.BooleanField(default=False)
#     is_superadmin        = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

#     objects = MyAccountManager()

#     def full_name(self):
#         return f'{self.first_name} {self.last_name}'

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return self.is_admin

#     def has_module_perms(self, add_label):
#         return True


# class UserProfile(models.Model):
#     user = models.OneToOneField(Account, on_delete=models.CASCADE)
#     address_line_1 = models.CharField(blank=True, max_length=100)
#     address_line_2 = models.CharField(blank=True, max_length=100)
#     profile_picture = models.ImageField(blank=True, upload_to='userprofile')
#     city = models.CharField(blank=True, max_length=20)
#     state = models.CharField(blank=True, max_length=20)
#     country = models.CharField(blank=True, max_length=20)

#     def __str__(self):
#         return self.user.first_name

#     def full_address(self):
#         return f'{self.address_line_1} {self.address_line_2}'

class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(default=datetime.datetime.now)


    def __str__(self):
        return self.wishlist_id

class WishlistItem(models.Model):
    # user = models.ForeignKey(register, on_delete=models.CASCADE, null=True)
    user_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    # product = models.ForeignKey(add_product, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    product_image=models.CharField(max_length=191,null=True, blank=True)
    product_name=models.TextField(max_length=191)
    Description=models.TextField(max_length=2000)
    Price=models.IntegerField()
    wishlist_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.Price * self.quantity




class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(default=datetime.datetime.now)


    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    # user = models.ForeignKey(register, on_delete=models.CASCADE, null=True)
    user_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    # product = models.ForeignKey(add_product, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    product_image=models.CharField(max_length=191,null=True, blank=True)
    product_name=models.TextField(max_length=191)
    Description=models.TextField(max_length=2000)
    Price=models.IntegerField()
    cart_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.Price * self.quantity

    # def __unicode__(self):
    #     return self.product
    
    # def __str__(self):
    #     return self.product_id


# class CItem(models.Model):
#     # user = models.ForeignKey(register, on_delete=models.CASCADE, null=True)
#     product = models.ForeignKey(add_product, on_delete=models.CASCADE)
#     # product_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
#     # variations = models.ManyToManyField(Variation, blank=True)
#     cart_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
#     quantity = models.IntegerField()
#     is_active = models.BooleanField(default=True)

#     # def sub_total(self):
#     #     return self.product.Price * self.quantity

#     # def __unicode__(self):
#     #     return self.product
    
#     def __str__(self):
#         return self.product

class Profile(models.Model):

    user_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    