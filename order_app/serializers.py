from rest_framework import serializers
from .models import OrderDetail, Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"
class ProductToOrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = OrderDetail
        fields = "__all__"