# Generated by Django 4.2.4 on 2023-08-30 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_useradditionalinformation_account_bal'),
    ]

    operations = [
        migrations.AddField(
            model_name='useradditionalinformation',
            name='activity_bal',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
