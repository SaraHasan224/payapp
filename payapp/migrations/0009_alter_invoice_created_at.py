# Generated by Django 5.0.4 on 2024-04-30 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0008_invoice_action_alter_invoice_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
