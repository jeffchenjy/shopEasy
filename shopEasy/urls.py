"""
URL configuration for shopEasy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include  # 要導入這個include
from myapp.views import *

from django.conf import settings
from django.conf.urls.static import static
# Use Rest API
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'merchandises', MerchandiseViewSet)
#router.register(r'members', MemberViewSet)


urlpatterns = [
    path('', goToLogin),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('member/login/', MemberLoginView.as_view(), name='memberLogin'),
    path('getmemberdata/', MemberDataView.as_view(), name='getMemberData'),
    path('edit/memberinfo/', UpdateMemberInfo.as_view(), name='editMemberInfo'),
    path('delete/member/', DeleteMember.as_view(), name='deleteMember'),
    path('upload/image/', UploadMemberImageView.as_view(), name='uploadMemberImage'),
    path('like/merchandise/', AddLikeMerchandiseView.as_view(),name='likeMerchandise'),
    path('get/likemerchandise/', GetLikeMerchandiseView.as_view(),name='getlikeMerchandise'),
    path('delete/likemerchandise/', DeleteLikeMerchandiseView.as_view(),name='deleteLikeMerchandise'),
    path('addtocart/', AddToCartView.as_view(),name='addtocart'),
    path('getcart/', GetCartView.as_view(),name='getcart'),
    path('deletecartitem/', DeleteCartItemView.as_view(),name='deletecartitem'),
    # Database Manager
    path('admin/', admin.site.urls),
    path('add/', addData),
    path('edit/<int:id>/', edit),
    path('home/', home),
    path('Book/', book),
    path('Computer/', computer),
    path('Appliance/', appliance),
    path('Audio/', audio),
    path('delete/<int:id>/', delete),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

