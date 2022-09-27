from dataclasses import Field
from distutils.command.upload import upload
import os
from tabnanny import verbose
from unicodedata import category, name
from django.db import models
import numbers
from django.contrib.auth.models import User
import datetime
import uuid
from django.forms import FilePathField
from pymysql import NULL
from django.urls import reverse
from django.template.defaultfilters import slugify

import vendor
def filepath(request, filename):
    old_filename = filename
    timeNow=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename= "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

def Productsfilepath(request, filename):
    old_filename = filename
    timeNow=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename="addProducts/" + "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/addProducts', filename)

def Profilefilepath(request, filename):
    old_filename = filename
    timeNow=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename="Profile_image/" + "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/Profile_image', filename)

def Companyfilepath(request, filename):
    old_filename = filename
    timeNow=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename="Company_image/" + "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/Company_image', filename)

# Create your models here.
class register(models.Model):
    name=models.TextField(max_length=191)
    business_name=models.TextField(max_length=191)
    email=models.EmailField(unique=True, max_length=191)
    phone_no=models.BigIntegerField()
    password=models.CharField(max_length=800)
    vendor_id = models.CharField(max_length=100, null=True, blank=True, unique=True, default=uuid.uuid4)

    def _str_(self):
            return self.name

    @staticmethod
    def get_vendor_by_email(email):
        try:
            return register.objects.get(email=email)
        except:
            return False

    def isExists(self):
        if register.objects.filter(email=self.email):           #return true or false
            return True
        else:
            return False

    
    
class contact_info(models.Model):
    vendor_id =  models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4, unique=True)
    Person_name=models.TextField(max_length=191)
    profile_pic=models.ImageField(upload_to=Profilefilepath, null=True, blank=True)
    email=models.EmailField(max_length=191)
    designaton=models.TextField(max_length=191)
    mobile_no=models.BigIntegerField()
    whatsapp_no=models.BigIntegerField()
    company_name=models.TextField(max_length=191)
    company_logo=models.ImageField(upload_to=Companyfilepath, null=True, blank=True)
    year_established=models.IntegerField()
    ceo_name=models.TextField(max_length=191)
    website=models.URLField(max_length=200, null=True, blank=True, unique=True)
    instagram = models.TextField(max_length=191, null=True, blank=True, unique=True)
    facebook = models.TextField(max_length=191, null=True, blank=True, unique=True)
    address_line1=models.TextField(max_length=191)
    address_line2=models.TextField(max_length=191)
    pincode=models.IntegerField()
    city=models.TextField(max_length=191)
    state=models.TextField(max_length=191)
    country=models.TextField(max_length=191)
    landmark=models.TextField(max_length=191)
    about = models.TextField(max_length=1000,default=NULL)
    status = models.TextField(max_length=300, default="NotVerified")

    def isExists(self):
        if contact_info.objects.filter(email=self.email):           #return true or false
            return True
        else:
            return False

    def get_url(self):
        # return self.vendor_id
        return reverse('vendor_view', args=[self.vendor_id])

class add_product(models.Model):
    product_image=models.ImageField(upload_to=Productsfilepath, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    product_id = models.CharField(max_length=30, null=True, blank=True, unique=True, default=uuid.uuid4)
    vendor_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    product_name=models.TextField(max_length=191)
    Description=models.TextField(max_length=2000)
    Price=models.IntegerField()
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(editable=False, default=datetime.datetime.now)
    modified_date = models.DateTimeField(default=datetime.datetime.now)
    
    # slug = models.SlugField(max_length=200, unique=True)
    
    def _str_(self):
        return self.product_name

    def get_url(self):
        return reverse('product', args=[self.slug])


class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Placed', 'Placed'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    order_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    vendor_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    # user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=30, null=True, blank=True, unique=True, default=uuid.uuid4)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)

    def _str_(self):
        return self.product.product_name


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Placed', 'Placed'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    # user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    # payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4, unique=True)
    # order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(default=datetime.datetime.now)


    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def _str_(self):
        return self.first_name

class ReviewRating(models.Model):
    product_id = models.CharField(max_length=30, null=True, blank=True, unique=True, default=uuid.uuid4)
    user_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    subject=models.CharField(max_length=100, blank=True)
    review=models.TextField(max_length=500, blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=20, blank=True)
    status=models.BooleanField(default=True)
    create_at=models.DateTimeField(default=datetime.datetime.now)
    updated_at=models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.subject

class ReviewRating(models.Model):
    product_id = models.CharField(max_length=30, null=True, blank=True, unique=True, default=uuid.uuid4)
    user_id = models.CharField(max_length=100, null=True, blank=True, default=uuid.uuid4)
    subject=models.CharField(max_length=100, blank=True)
    review=models.TextField(max_length=500, blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=20, blank=True)
    status=models.BooleanField(default=True)
    create_at=models.DateTimeField(default=datetime.datetime.now)
    updated_at=models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.subject

# class ProductGallery(models.Model):
#     product_id = models.CharField(max_length=30, null=True, blank=True, unique=True, default=uuid.uuid4)
#     image=models.ImageField(upload_to=Productsfilepath, null=True, blank=True)

#     def __str__(self):
#         return self.product.product_name

    