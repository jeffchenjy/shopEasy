# Generated by Django 4.2.11 on 2024-05-03 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_member_cpassword_alter_member_cemail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='cImage',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
