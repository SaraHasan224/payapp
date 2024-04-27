# Generated by Django 5.0.4 on 2024-04-26 16:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0004_remove_profile_currency_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='currency_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payapp.currency'),
        ),
    ]