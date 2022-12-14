# Generated by Django 4.0.4 on 2022-06-12 15:45

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wishlist_id', models.CharField(blank=True, max_length=250)),
                ('date_added', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, default=uuid.uuid4, max_length=100, null=True)),
                ('product_id', models.CharField(blank=True, default=uuid.uuid4, max_length=100, null=True)),
                ('product_image', models.CharField(blank=True, max_length=191, null=True)),
                ('product_name', models.TextField(max_length=191)),
                ('Description', models.TextField(max_length=2000)),
                ('Price', models.IntegerField()),
                ('wishlist_id', models.CharField(blank=True, default=uuid.uuid4, max_length=100, null=True)),
                ('quantity', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
