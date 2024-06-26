# Generated by Django 4.2.11 on 2024-04-30 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_member_cnickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='cAddr',
            field=models.CharField(blank=True, default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='member',
            name='cCountry',
            field=models.CharField(blank=True, default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='member',
            name='cNickName',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='member',
            name='cPhone',
            field=models.CharField(blank=True, default='Unknown', max_length=20),
        ),
        migrations.AlterField(
            model_name='member',
            name='cSex',
            field=models.CharField(default='Unknown', max_length=7),
        ),
    ]
