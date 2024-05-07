# Generated by Django 4.2.11 on 2024-04-30 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_member_caddr_alter_member_cbirthday_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='cPassword',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='member',
            name='cEmail',
            field=models.EmailField(max_length=100),
        ),
        migrations.AlterField(
            model_name='member',
            name='cNickName',
            field=models.CharField(blank=True, default='Unknown', max_length=255),
        ),
        migrations.DeleteModel(
            name='memberPermissions',
        ),
    ]