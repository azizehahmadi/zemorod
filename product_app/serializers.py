from .models import ProductCategory, Product, RatingProduct
from rest_framework import serializers
from django.db.models import Avg


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ('id', 'title', 'is_active', 'is_delete')


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer
    class Meta:
        model = Product
        fields = ('id', 'title','category', 'price',
                  'short_description', 'description', 'is_active', 'is_delete', 'date_register', 'image')




class RatingProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = RatingProduct
        fields = ('id', 'product', 'user', 'rating', 'is_active', 'is_delete', 'comment', 'ip', 'created_at')



class ShortProductInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('title', 'short_description', 'image', 'price')



class CommentRatingForShortInfoSerializer(serializers.ModelSerializer):

    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = RatingProduct
        fields = ('comment', 'avg_rating')

    def get_avg_rating(self, instance):

        average = RatingProduct.objects.filter(product=instance.product).aggregate(Avg('rating'))

        if average is not None:
            return {'avg_rating': round(average['rating__avg'], 2)}
        return None

