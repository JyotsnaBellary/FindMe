# Generated by Django 3.2.4 on 2022-05-27 12:47

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(blank=True, max_length=250)),
                ('date_added', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, default=uuid.uuid4, max_length=100, null=True)),
                ('product_id', models.CharField(blank=True, default=uuid.uuid4, max_length=100, null=True)),
                ('product_image', models.CharField(blank=True, max_length=191, null=True)),
                ('product_name', models.TextField(max_length=191)),
                ('Description', models.TextField(max_length=2000)),
                ('Price', models.IntegerField()),
                ('cart_id', models.CharField(blank=True, default=uuid.uuid4, max_length=100, null=True)),
                ('quantity', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, default=uuid.uuid4, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=26)),
                ('username', models.CharField(blank=True, max_length=26)),
                ('email', models.CharField(blank=True, max_length=26)),
                ('password', models.CharField(blank=True, max_length=220)),
            ],
            options={
                'unique_together': {('username', 'email')},
            },
        ),
    ]
