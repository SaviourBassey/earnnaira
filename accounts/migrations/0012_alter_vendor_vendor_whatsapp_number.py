# Generated by Django 4.2.4 on 2023-08-27 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_remove_vendor_vendor_whatsapp_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vendor_whatsapp_number',
            field=models.CharField(max_length=10),
        ),
    ]
