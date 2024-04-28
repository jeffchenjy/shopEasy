from django.shortcuts import *
from django.http import *
from myapp.models import *
from django.forms.models import model_to_dict
import os
from django.conf import settings
from datetime import datetime
from django.contrib.auth.decorators import login_required
# Use Rest API
from rest_framework import viewsets
from .models import merchandise
from .serializers import MerchandiseSerializer
class MerchandiseViewSet(viewsets.ModelViewSet):
    queryset = merchandise.objects.all()
    serializer_class = MerchandiseSerializer
# Create your views here.
def goToLogin(request):
    return redirect('/admin/')
def home(request):
    if not request.user.is_authenticated:
        return redirect('/admin/')
    datas = merchandise.objects.all().order_by("cID")
    return render(request, 'home.html', locals())

def book(request):
    if not request.user.is_authenticated:
        return redirect('/admin/')
    title = "Book"
    datas = merchandise.objects.filter(cSort='Book').order_by("cID")
    return render(request, 'sort.html', locals())

def computer(request):
    if not request.user.is_authenticated:
        return redirect('/admin/')
    title = "Computer"
    datas = merchandise.objects.filter(cSort='Computer').order_by("cID")
    return render(request, 'sort.html', locals())

def appliance(request):
    if not request.user.is_authenticated:
        return redirect('/admin/')
    title = "Appliance"
    datas = merchandise.objects.filter(cSort='Appliance').order_by("cID")
    return render(request, 'sort.html', locals())

def audio(request):
    if not request.user.is_authenticated:
        return redirect('/admin/')
    title = "Audio"
    datas = merchandise.objects.filter(cSort='Audio').order_by("cID")
    return render(request, 'sort.html', locals())

def addData(request):
    if not request.user.is_authenticated:
        return redirect('/admin/')
    error = ''
    if request.method == "POST":
        cName = request.POST["cName"]
        cAuthor = request.POST["cAuthor"]
        cCompany = request.POST["cCompany"]
        cSort = request.POST["cSort"]
        cClass = request.POST["cClass"]
        cPrice = request.POST["cPrice"]
        cDate = request.POST.get('cDate')
        cDate = datetime.strptime(cDate, '%Y-%m-%d').date()
        cDescription = request.POST["cDescription"]
        add = merchandise(cName=cName, cAuthor=cAuthor, cCompany=cCompany, cClass=cClass, cPrice=cPrice, cSort=cSort, cDate=cDate, cDescription=cDescription)
        if (request.FILES.get('image') != None):
            img = request.FILES.get('image')
            pic_name = img.name  # 先取得圖片檔案名稱
            if pic_name.split('.')[-1] == 'mp4':
                error = '暫不支援上傳此格式圖片！！！'
            else:
                add = merchandise(cName=cName, cAuthor=cAuthor, cCompany=cCompany, cClass=cClass, cPrice=cPrice, cSort=cSort, cDate=cDate, cDescription=cDescription, cImageName=pic_name, cImage=img)
        add.save()
        return redirect('/home/')
    else:
        return render(request, "add.html", locals())
def edit(request, id=None):
    if not request.user.is_authenticated:
        return redirect('/admin/')
    error = ''
    if request.method == 'POST':
        cName = request.POST["cName"]
        cAuthor = request.POST["cAuthor"]
        cCompany = request.POST["cCompany"]
        cSort = request.POST["cSort"]
        cClass = request.POST["cClass"]
        cPrice = request.POST["cPrice"]
        cDate = request.POST.get('cDate')
        cDate = datetime.strptime(cDate, '%Y-%m-%d').date()
        cDescription = request.POST["cDescription"]
        update = merchandise.objects.get(cID=id)
        update.cName = cName
        update.cAuthor = cAuthor
        update.cCompany = cCompany
        update.cSort = cSort
        update.cClass = cClass
        update.cPrice = cPrice
        update.cDate = cDate
        update.cDescription = cDescription
        if (request.FILES.get('image') != None):
            img = request.FILES.get('image')
            pic_name = img.name
            if pic_name.split('.')[-1] == 'mp4':
                error = '暫不支援上傳此格式圖片！！！'
            else:
                update.cImageName=pic_name
                update.cImage=img
                update.save()
            return redirect('/home/')
        else:
            update.save()
            return redirect('/home/')
    else:
        data = merchandise.objects.get(cID=id)
        return render(request, "edit.html", locals())
def delete(request, id=None):
    if not request.user.is_authenticated:
        return redirect('/admin/')
    if request.method == "POST":
        data = merchandise.objects.get(cID=id)
        image_path = os.path.join(settings.MEDIA_ROOT, 'pictures', data.cImageName)
        # 刪除圖片文件
        if os.path.exists(image_path):
            os.remove(image_path)
        data.delete()
        return redirect("/home/")
    else :
        data = merchandise.objects.get(cID=id)
        return render(request, "delete.html", locals())
