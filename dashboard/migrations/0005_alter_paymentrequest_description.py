# Generated by Django 4.2.4 on 2023-08-30 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_paymentrequest_account_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrequest',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]