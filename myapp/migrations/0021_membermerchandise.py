# Generated by Django 4.2.11 on 2024-05-08 10:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_delete_membermerchandise'),
    ]

    operations = [
        migrations.CreateModel(
            name='memberMerchandise',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cLikeMerchandiseList', models.JSONField()),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.member')),
            ],
        ),
    ]
