from rest_framework import serializers
from .models import OrderDetail, Order, RegisterOrder


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"
class ProductToOrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = OrderDetail
        fields = "__all__"


class RegisterOrderSerializer(serializers.ModelSerializer):
    town = serializers.ReadOnlyField(source='user_profile.town')
    country = serializers.ReadOnlyField(source='user_profile.country')
    code_post = serializers.ReadOnlyField(source='user_profile.code_post')
    phone = serializers.ReadOnlyField(source='user_profile.phone')
    class Meta:
        model = RegisterOrder
        fields = ('title', 'count', 'color', 'town', 'country', 'code_post', 'phone')