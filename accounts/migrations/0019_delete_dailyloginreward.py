# Generated by Django 4.2.4 on 2023-08-31 01:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_useradditionalinformation_activity_bal'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DailyLoginReward',
        ),
    ]