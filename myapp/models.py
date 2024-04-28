from django.db import models
from django.contrib.auth.models import AbstractUser
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