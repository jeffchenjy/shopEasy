from rest_framework import serializers
from .models import merchandise

class MerchandiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = merchandise
        fields = '__all__'