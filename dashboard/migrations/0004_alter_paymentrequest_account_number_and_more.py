# Generated by Django 4.2.4 on 2023-08-30 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_paymentrequest_account_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrequest',
            name='account_number',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='bank_name',
            field=models.CharField(max_length=255),
        ),
    ]
