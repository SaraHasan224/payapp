# Generated by Django 5.0.4 on 2024-04-30 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0007_rename_invoice_id_notification_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='action',
            field=models.CharField(choices=[('0', 'Void'), ('1', 'Credit'), ('2', 'Debit')], default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('0', 'Draft'), ('1', 'Sent'), ('2', 'Processing'), ('3', 'Processed'), ('4', 'Rejected')], default='0', max_length=1),
        ),
    ]
