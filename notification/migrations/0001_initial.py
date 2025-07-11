# Generated by Django 5.0.13 on 2025-07-10 12:46

import django.db.models.deletion
import utils.functions
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.CharField(max_length=128)),
                ('updated_by', models.CharField(max_length=128)),
                ('updated_dtm', models.DateTimeField(auto_now=True)),
                ('created_dtm', models.DateTimeField(auto_now_add=True)),
                ('deleted_dtm', models.DateTimeField(default=None, null=True)),
                ('notification_id', models.CharField(default=utils.functions.get_uuid, max_length=128, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('notification_data', models.JSONField(blank=True, null=True)),
                ('notification_type_id', models.CharField(choices=[('INVOICE', 'Invoice'), ('PAYMENT', 'Payment')], max_length=64)),
            ],
            options={
                'db_table': 'notification',
            },
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.CharField(max_length=128)),
                ('updated_by', models.CharField(max_length=128)),
                ('updated_dtm', models.DateTimeField(auto_now=True)),
                ('created_dtm', models.DateTimeField(auto_now_add=True)),
                ('deleted_dtm', models.DateTimeField(default=None, null=True)),
                ('user_notification_id', models.CharField(default=utils.functions.get_uuid, max_length=128, primary_key=True, serialize=False)),
                ('is_read', models.BooleanField(default=False)),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='notification.notification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_notification_mapping',
            },
        ),
    ]
