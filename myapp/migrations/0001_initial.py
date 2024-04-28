# Generated by Django 4.2.11 on 2024-04-28 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='merchandise',
            fields=[
                ('cID', models.AutoField(primary_key=True, serialize=False)),
                ('cName', models.CharField(max_length=254)),
                ('cAuthor', models.CharField(max_length=100, null=True)),
                ('cCompany', models.CharField(max_length=100, null=True)),
                ('cSort', models.CharField(max_length=100)),
                ('cClass', models.CharField(max_length=100)),
                ('cPrice', models.IntegerField(null=True)),
                ('cDate', models.DateTimeField(auto_now_add=True)),
                ('cImageName', models.CharField(max_length=254, null=True)),
                ('cImage', models.ImageField(null=True, upload_to='pictures')),
                ('cDescription', models.TextField(null=True)),
            ],
        ),
    ]
