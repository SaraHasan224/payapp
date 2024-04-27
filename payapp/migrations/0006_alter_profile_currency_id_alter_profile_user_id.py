# Generated by Django 5.0.4 on 2024-04-26 18:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0005_profile_currency_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='currency_id',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='payapp.currency'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_id',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]