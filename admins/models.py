from django.db import models

# Create your models here.
class register(models.Model):
    # class for customers
    username = models.CharField(max_length=26, blank=True)
    email = models.CharField(max_length=26, blank=True)
    password = models.CharField(max_length=220, blank=True)

    