# Generated by Django 5.0.4 on 2024-04-29 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0004_alter_invoice_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_no',
            field=models.CharField(max_length=255),
        ),
    ]
