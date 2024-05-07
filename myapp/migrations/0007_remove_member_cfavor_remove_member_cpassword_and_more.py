# Generated by Django 4.2.11 on 2024-04-30 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_member_cfavor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='cFavor',
        ),
        migrations.RemoveField(
            model_name='member',
            name='cPassword',
        ),
        migrations.AlterField(
            model_name='member',
            name='cSex',
            field=models.CharField(default='N', max_length=3),
        ),
        migrations.CreateModel(
            name='memberPermissions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('passwd', models.CharField(max_length=100)),
                ('level', models.CharField(max_length=2)),
                ('cID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.member')),
            ],
        ),
        migrations.CreateModel(
            name='memberMerchandise',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cFavor', models.TextField(null=True)),
                ('cRank', models.CharField(max_length=3, null=True)),
                ('cID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.member')),
            ],
        ),
    ]
