# Generated by Django 4.0.4 on 2022-06-12 11:57

from django.db import migrations, models
import vendor.models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_reviewrating_orderproduct_vendor_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Placed', 'Placed'), ('Accepted', 'Accepted'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='New', max_length=10),
        ),
        migrations.AlterField(
            model_name='contact_info',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to=vendor.models.Companyfilepath),
        ),
        migrations.AlterField(
            model_name='contact_info',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=vendor.models.Profilefilepath),
        ),
    ]