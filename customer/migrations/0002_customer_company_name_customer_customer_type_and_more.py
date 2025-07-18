# Generated by Django 5.0.13 on 2025-06-03 10:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='company_name',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='customer_type',
            field=models.CharField(choices=[('BUSINESS', 'Business'), ('INDIVIDUAL', 'Individual')], default=django.utils.timezone.now, max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]
