# Generated by Django 4.2.11 on 2024-04-28 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_merchandise_cid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchandise',
            name='cID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]