from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone
#pip install mysqlclient
#python manage.py makemigrations  
#python manage.py migrate

class merchandise(models.Model): #資料庫名稱
    cID = models.AutoField(primary_key=True) #資料庫表格名稱
    cName = models.CharField(max_length=254, blank=False)
    cAuthor = models.CharField(max_length=100, blank=False, null=True)
    cCompany = models.CharField(max_length=100, blank=False, null=True)
    cSort = models.CharField(max_length=100, blank=False)
    cClass = models.CharField(max_length=100, blank=False)
    cPrice = models.IntegerField(null=True)
    cDate = models.DateTimeField(auto_now_add=True)
    cImageName = models.CharField(max_length=254, null=True)
    cImage = models.ImageField(upload_to='pictures', null=True)
    cDescription = models.TextField(null=True)
    cInventory = models.IntegerField(default=0)

class member(models.Model): #資料庫名稱
    cID = models.AutoField(primary_key=True) #資料庫表格名稱
    cName = models.CharField(max_length=255, blank=False)
    cNickName = models.CharField(max_length=255, blank=True, default='Unknown')
    cEmail = models.EmailField(max_length=100, blank=False)
    cPassword = models.CharField(max_length=100, blank=True)
    cPhone = models.CharField(max_length=20, blank=True, default='Unknown')
    cAddr = models.CharField(max_length=255, blank=True, default='Unknown')
    cCountry = models.CharField(max_length=255, blank=True, default='Unknown')
    cBirthday = models.DateField(null=True)
    cSex = models.CharField(max_length=7, default='Unknown')
    cImageName = models.CharField(max_length=254, null=True)
    cImage = models.ImageField(upload_to='images', null=True)
    
class memberMerchandise(models.Model):
    id = models.AutoField(primary_key=True)
    merchandise = models.ForeignKey('merchandise', on_delete=models.CASCADE)
    cRank = models.IntegerField(null=True)
    member = models.ForeignKey('member', on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=django.utils.timezone.now)
    class Meta:
        unique_together = (('member', 'merchandise'),)

class memberOrder(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey('member', on_delete=models.CASCADE)
    cMerchandiseList = models.JSONField()
    cPayment = models.CharField(max_length=20, default='Cash')
    created_time = models.DateTimeField(default=django.utils.timezone.now)