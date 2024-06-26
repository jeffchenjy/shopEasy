from rest_framework import serializers
from .models import merchandise, member, memberMerchandise, memberCart, memberOrder

class MerchandiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = merchandise
        fields = '__all__'
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = member
        fields = '__all__'
class MemberMerchandiseSerializer(serializers.ModelSerializer):
     class Meta:
        model = memberMerchandise
        fields = '__all__'
class MemberCartSerializer(serializers.ModelSerializer):
     class Meta:
        model = memberCart
        fields = '__all__'
class MemberOrderSerializer(serializers.ModelSerializer):
     class Meta:
        model = memberOrder
        fields = '__all__'