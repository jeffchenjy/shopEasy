# Generated by Django 4.2.11 on 2024-05-06 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_membermerchandise_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchandise',
            name='cInventory',
            field=models.IntegerField(default=0),
        ),
    ]
