# Generated by Django 4.2.4 on 2023-08-23 16:46

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SponsoredPost',
            new_name='Post',
        ),
        migrations.RenameModel(
            old_name='SponsoredPostCategory',
            new_name='PostCategory',
        ),
    ]
