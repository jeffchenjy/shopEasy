from django.shortcuts import *
from django.http import *
from myapp.models import *
from django.forms.models import model_to_dict
import os
from django.conf import settings
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
# API Auth
from django.contrib.auth import authenticate
from rest_framework.views import APIView
#API權限
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication 
#密碼加密
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
# Use Rest API
from rest_framework import viewsets
from .models import *
from .serializers import MerchandiseSerializer, MemberSerializer, MemberMerchandiseSerializer, MemberCartSerializer, MemberOrderSerializer
# API View 
class MerchandiseViewSet(viewsets.ModelViewSet):
    queryset = merchandise.objects.all()
    serializer_class = MerchandiseSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
class MemberViewSet(viewsets.ModelViewSet):
    queryset = member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
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
        cInventory = request.POST["cInventory"]
        add = merchandise(cName=cName, cAuthor=cAuthor, cCompany=cCompany, cClass=cClass, cPrice=cPrice, 
                          cSort=cSort, cDate=cDate, cDescription=cDescription, cInventory=cInventory)
        if (request.FILES.get('image') != None):
            img = request.FILES.get('image')
            pic_name = img.name  # 先取得圖片檔案名稱
            if pic_name.split('.')[-1] == 'mp4':
                error = '暫不支援上傳此格式圖片！！！'
            else:
                add = merchandise(cName=cName, cAuthor=cAuthor, cCompany=cCompany, cClass=cClass, cPrice=cPrice, cSort=cSort, 
                                  cDate=cDate, cDescription=cDescription, cImageName=pic_name, cImage=img, cInventory=cInventory)
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
        cInventory = request.POST["cInventory"]
        update = merchandise.objects.get(cID=id)
        update.cName = cName
        update.cAuthor = cAuthor
        update.cCompany = cCompany
        update.cSort = cSort
        update.cClass = cClass
        update.cPrice = cPrice
        update.cDate = cDate
        update.cDescription = cDescription
        update.cInventory = cInventory
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

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class RegisterView(APIView):
    def post(self, request, format=None):
        #獲取使用者未加密密碼
        password = request.data.get('cPassword')
        #加密密碼
        hashed_password = make_password(password)
        #將加密的密碼更新至POST Data之中
        request.data['cPassword'] = hashed_password
        email = request.data.get('cEmail')
        #使用 serializer 進行數據的驗證與保存
        serializer = MemberSerializer(data=request.data)
        if member.objects.filter(cEmail=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MemberLoginView(APIView):
    def post(self, request, format=None):
        cEmail = request.data.get('cEmail')
        cPassword = request.data.get('cPassword')
        try:
            # 取得與提供的使用者名稱相符的使用者對象
            user = member.objects.get(cEmail=cEmail)
            # 檢查使用者提供的密碼是否與資料庫中儲存的哈希密碼(Hashing Password)相符
            if check_password(cPassword, user.cPassword):
                serializer = MemberSerializer(user)
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            else:
                # 如果失敗，則使用者提供的使用者名稱或密碼錯誤
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except member.DoesNotExist:
            # 如果找不到與提供的使用者名稱相符的使用者對象，則傳回使用者名稱或密碼錯誤
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class MemberChangePasswordView(APIView):
    def post(self, request, format=None):
        info = request.data
        cEmail = info.get('cEmail')
        try:
            # 取得與提供的使用者名稱相符的使用者對象
            user = member.objects.get(cEmail=cEmail)
            if info.get('cPassword') is not None:
                try :
                    password = info.get('cPassword')
                    hashed_password = make_password(password)
                    info['cPassword'] = hashed_password
                    serializer = MemberSerializer(user, data=info, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'message': 'Password change successful'}, status=status.HTTP_200_OK)
                except :
                    return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Email verification successful'}, status=status.HTTP_200_OK)
        except member.DoesNotExist:
            # 如果找不到與提供的使用者名稱相符的使用者對象，則傳回錯誤
            return Response({'error': 'メンバーが存在しません。もう一度電子メールを入力してください。'}, status=status.HTTP_404_NOT_FOUND)
class GetMemberDataView(APIView):
    def post(self, request):
        # 獲取email參數
        email = request.data.get('cEmail')
        # 查詢資料
        try:
            user = member.objects.get(cEmail=email)
            serializer = MemberSerializer(user)
            return JsonResponse(serializer.data)
        except member.DoesNotExist:
            return JsonResponse({'error': 'Member not found'}, status=404)
class UpdateMemberInfo(APIView):
    def post(self, request):
        new_info = request.data
        # 獲取Member信箱
        email = new_info.get('cEmail')
        if new_info.get('cPassword') is not None:
            try :
                password = new_info.get('cPassword')
                hashed_password = make_password(password)
                new_info['cPassword'] = hashed_password
            except :
                print("Invalid password")
        if new_info.get('cBirthday') is not None:
            try:
                birthday_str = request.data.get('cBirthday')
                birthday_date = datetime.strptime(birthday_str, '%Y-%m-%d').date()
                new_info['cBirthday'] = birthday_date
            except ValueError:
                return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic(): #保證更新的一致性
            try:
                # 在資料庫中查找用户
                user = member.objects.select_for_update().get(cEmail=email)
            except member.DoesNotExist:
                return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
            #使用 serializer 進行數據的驗證與更新
            serializer = MemberSerializer(user, data=new_info, partial=True)
            if serializer.is_valid():
                    serializer.save()
                    updateData = member.objects.get(cEmail=email)
                    serializer = MemberSerializer(updateData)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
class UploadMemberImageView(APIView):
    def post(self, request):
        if 'image' in request.FILES:
            email = request.data.get('email')
            image = request.FILES['image']
            pic_name = image.name
            update = member.objects.get(cEmail = email)
            try : 
                image_path = os.path.join(settings.MEDIA_ROOT, 'images', update.cImageName)
                # 刪除圖片文件
                if os.path.exists(image_path):
                    os.remove(image_path)
            except member.DoesNotExist:
                print("No such member exists")
                return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
            update.cImage = image
            update.cImageName = pic_name
            update.save()
            updateData = member.objects.get(cEmail=email)
            serializer = MemberSerializer(updateData)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No image provided'}, status=status.HTTP_404_NOT_FOUND)
class DeleteMember(APIView):
    def post(self, request):
        email = request.data.get('cEmail')
        try:
            user = member.objects.get(cEmail=email)
            image_path = os.path.join(settings.MEDIA_ROOT, 'images', user.cImageName)
            # 刪除圖片文件
            if os.path.exists(image_path):
                os.remove(image_path)
            user_id = user.pk
            user_data = memberMerchandise.objects.filter(member_id=user_id)
            if user_data:
                user_data.delete()
            user.delete()
            return Response({'message': 'Delete successful'})
        except member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=404)
class AddLikeMerchandiseView(APIView):
      def post(self, request):
        email = request.data.get('cEmail')
        merchandise_id = request.data.get('merchandise_id')
        try:
            user = member.objects.get(cEmail=email)
            user_id = user.pk
            item = merchandise.objects.get(cID = merchandise_id)
            merchandise_name = item.cName
            try:
                like_entry = memberMerchandise.objects.get(member_id=user_id)
                like_data = like_entry.cLikeMerchandiseList
            except memberMerchandise.DoesNotExist:
                # 如果資料不存在，建立一個新的資料
                like_entry = memberMerchandise.objects.create(member_id=user_id, cLikeMerchandiseList={})
                like_data = {}
            if merchandise_id in like_data:
                # 如果存在，則什麼都不做，返回
                return Response({'error': 'Member already likes this merchandise'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # 如果不存在，則新增商品
                current_time = timezone.now().date()
                like_data[merchandise_id] = {
                    'name': merchandise_name,
                    'addedDate': current_time.isoformat()
                }
            like_entry.cLikeMerchandiseList = like_data
            like_entry.save()
            #返回喜愛項目資料
            update_member_like = memberMerchandise.objects.get(member_id=user_id)
            serializer = MemberMerchandiseSerializer(update_member_like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except merchandise.DoesNotExist:
            return Response({'error': 'Merchandise not found'}, status=status.HTTP_404_NOT_FOUND)
        except member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
class GetLikeMerchandiseView(APIView):
    def post(self, request):
        email =  request.data.get('cEmail')
        try:
            user = member.objects.get(cEmail=email)
            user_id = user.pk
            try:
                #返回喜愛項目資料
                member_like = memberMerchandise.objects.get(member_id=user_id)
                serializer = MemberMerchandiseSerializer(member_like)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except memberMerchandise.DoesNotExist:
                # 如果喜愛項目資料不存在，返回錯誤
                return Response({'error': 'Like not found'}, status=status.HTTP_404_NOT_FOUND)
        except member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
class DeleteLikeMerchandiseView(APIView):
    def post(self, request):
        email = request.data.get('cEmail')
        merchandise_id = request.data.get('merchandiseID')
        try: 
            user = member.objects.get(cEmail=email)
            user_id = user.pk
            try:
                member_like = memberMerchandise.objects.get(member_id=user_id)
                likemerchandise_list = member_like.cLikeMerchandiseList
                if merchandise_id in likemerchandise_list:
                    del likemerchandise_list[merchandise_id]
                    member_like.save()
                    #返回喜愛項目資料
                    update_member_like = memberMerchandise.objects.get(member_id=user_id)
                    serializer = MemberMerchandiseSerializer(update_member_like)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)
            except memberMerchandise.DoesNotExist:
                # 如果喜愛項目資料不存在，返回錯誤
                return Response({'error': 'Like not found'}, status=status.HTTP_404_NOT_FOUND)
        except member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
class AddToCartView(APIView):
    def post(self, request):
        newData = request.data
        email = newData.get('cEmail')
        merchandise_id = newData.get('cID')
        merchandise_name = newData.get('cName')
        merchandise_price = newData.get('cPrice')
        quantity = newData.get('quantity')
        try: 
            user = member.objects.get(cEmail=email)
            user_id = user.pk
            try:
                cart_entry = memberCart.objects.get(member_id=user_id)
                cart_data = cart_entry.cMerchandiseList
            except memberCart.DoesNotExist:
                # 如果購物車不存在，建立一個新的購物車
                cart_entry = memberCart.objects.create(member_id=user_id, cMerchandiseList={})
                cart_data = {}
            if merchandise_id in cart_data:
                # 如果存在，則更新商品數量
                cart_data[merchandise_id]['quantity'] = int(quantity)
            else:
                # 如果不存在，則新增商品
                current_time = timezone.now().date()
                cart_data[merchandise_id] = {
                    'name': merchandise_name,
                    'price': merchandise_price,
                    'quantity': int(quantity),
                    'addedDate': current_time.isoformat()
                }
            cart_entry.cMerchandiseList = cart_data
            cart_entry.save()
            #返回購物車資料
            update_member_cart = memberCart.objects.get(member_id=user_id)
            serializer = MemberCartSerializer(update_member_cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
class GetCartView(APIView):
    def post(self, request):
        email = request.data.get('cEmail')
        try: 
            user = member.objects.get(cEmail=email)
            user_id = user.pk
            try:
                #返回購物車資料
                member_cart = memberCart.objects.get(member_id=user_id)
                serializer = MemberCartSerializer(member_cart)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except memberCart.DoesNotExist:
                # 如果購物車不存在，返回錯誤
                return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        except member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
        
class DeleteCartItemView(APIView):
    def post(self, request):
        email = request.data.get('cEmail')
        merchandise_id = request.data.get('cID')
        try: 
            user = member.objects.get(cEmail=email)
            user_id = user.pk
            try:
                member_cart = memberCart.objects.get(member_id=user_id)
                merchandise_list = member_cart.cMerchandiseList
                if merchandise_id in merchandise_list:
                    del merchandise_list[merchandise_id]
                    member_cart.save()
                    #返回購物車資料
                    update_member_cart = memberCart.objects.get(member_id=user_id)
                    serializer = MemberCartSerializer(update_member_cart)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)
            except memberCart.DoesNotExist:
                # 如果購物車不存在，返回錯誤
                return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        except member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

class CreateOrderView(APIView):
    def post(self, request):
        newData = request.data
        # 訂購資訊
        name = newData.get('customerName')
        email = newData.get('customerEmail')
        phone = newData.get('customerPhone')
        recipientName = newData.get('recipientName')
        recipientEmail = newData.get('recipientEmail')
        recipientPhone = newData.get('recipientPhone')
        shippingAddress = newData.get('shippingAddress')
        shippingMethod = newData.get('shippingMethod')
        payment = newData.get('payment')
        deliveryTime = newData.get('deliveryTime')
        # 商品資訊
        merchandise_data = newData.get('merchandise')
        totalQuantity = newData.get('totalQuantity')
        totalPrice = newData.get('totalPrice')
        try: 
            user = member.objects.get(cEmail=email)
            user_id = user.pk
            #建立訂單
            order_entry = memberOrder.objects.create(member_id=user_id, orderInfo={})
            order_data = {
                'merchandise': {}  # 初始化 merchandise 鍵的值為一個空字典
            }
            current_time = timezone.now().strftime('%Y-%m-%d')  # 將日期轉換為字串
            for item_info in merchandise_data:
                item_id = item_info[0]  # 商品ID
                item_name = item_info[1]  # 商品名稱
                item_price = item_info[2]  # 商品價格
                item_quantity = item_info[3]  # 商品數量
                item_addedDate = item_info[4]  # 商品新增日期
                order_data['merchandise'][item_id] = {
                    'name': item_name,
                    'price': item_price,
                    'quantity': int(item_quantity),
                    'addedDate': item_addedDate,
                }
            order_data['customer'] = {
                'name': name,
                'email': email,
                'phone': phone,
            }
            order_data['recipient'] = {
                'name': recipientName,
                'email': recipientEmail,
                'phone': recipientPhone,
            }
            order_data['shipping'] = {
                'shippingMethod': shippingMethod,
                'shippingAddress': shippingAddress,
                'deliveryTime': deliveryTime,
            }
            order_data['payment'] = {
                'totalQuantity': totalQuantity,
                'totalPrice': totalPrice,
                'payment': payment,
            }
            order_data['createTime'] = current_time
            order_entry.orderInfo = order_data
            order_entry.save()

            #清除購物車資料
            try:
                member_cart = memberCart.objects.get(member_id=user_id)
                member_cart.delete()
                try:
                    #返回訂單資料
                    member_orders = memberOrder.objects.filter(member_id=user_id)
                    serializer = MemberOrderSerializer(member_orders, many=True)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except memberOrder.DoesNotExist:
                # 如果訂單不存在，返回錯誤
                    return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
            except memberCart.DoesNotExist:
                return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        except member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
class GetOrderView(APIView):
    def post(self, request):
        email = request.data.get('cEmail')
        try: 
            user = member.objects.get(cEmail=email)
            user_id = user.pk
            try:
                #返回訂單資料
                member_orders = memberOrder.objects.filter(member_id=user_id)
                serializer = MemberOrderSerializer(member_orders, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except memberOrder.DoesNotExist:
                # 如果訂單不存在，返回錯誤
                return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        except member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
class DeleteOrderView(APIView):
    def post(self, request):
        id = request.data.get('orderID')
        email = request.data.get('cEmail')
        try: 
            user = member.objects.get(cEmail=email)
            user_id = user.pk
            try:
                #刪除訂單資料
                member_orders = memberOrder.objects.filter(member_id=user_id, id = id)
                member_orders.delete()
                #返回訂單資料
                renew_member_orders = memberOrder.objects.filter(member_id=user_id)
                serializer = MemberOrderSerializer(renew_member_orders, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except memberOrder.DoesNotExist:
                # 如果訂單不存在，返回錯誤
                return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        except member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)