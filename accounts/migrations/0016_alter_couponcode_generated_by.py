# Generated by Django 4.2.4 on 2023-08-27 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_couponcode_generated_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponcode',
            name='generated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.vendor'),
        ),
    ]
