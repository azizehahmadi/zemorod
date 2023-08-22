import datetime

from rest_framework.views import APIView
from product_app.models import ProductCategory, Product
from rest_framework import status
from rest_framework.response import Response
from product_app.serializers import ProductSerializer
from django.db.models import Avg, Max, Count, Sum
from order_app.models import OrderDetail

class GlobalSearch_dynamic(APIView):

    def get(self, request):

        search_query = request.query_params.get('q', '')

        product_base_on_category_result = Product.objects.filter(is_active=True, is_delete=False,
                                                                     category__title__icontains=search_query,
                                                                 category__is_delete=False, category__is_active=True)

        product_base_on_title_result = Product.objects.filter(title__icontains=search_query, is_active=True,
                                                              is_delete=False)

        response_data = {}

        if product_base_on_category_result.exists():
            product_base_category_serializer = ProductSerializer(product_base_on_category_result, many=True)
            response_data['product_category'] = product_base_category_serializer.data

        if product_base_on_title_result.exists():
            product_base_title_serializer = ProductSerializer(product_base_on_title_result, many=True)
            response_data['product_title'] = product_base_title_serializer.data

        if not response_data:
            return Response({'msg': 'No results found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(response_data, status=status.HTTP_200_OK)


class cheapestProduct(APIView):

    def get(self, request):
        cheap_product = Product.objects.filter(is_delete=False, is_active=True).order_by('price')[:2]

        if cheap_product.exists():
            CheapProductSerializer = ProductSerializer(cheap_product, many=True)
            return Response(CheapProductSerializer.data, status=status.HTTP_200_OK)
        return Response({'msg': 'No product found'}, status=status.HTTP_404_NOT_FOUND)


class expensiveProduct(APIView):

    def get(self, request):
        cheap_product = Product.objects.filter(is_delete=False, is_active=True).order_by('-price')[:2]

        if cheap_product.exists():
            CheapProductSerializer = ProductSerializer(cheap_product, many=True)
            return Response(CheapProductSerializer.data, status=status.HTTP_200_OK)
        return Response({'msg': 'No product found'}, status=status.HTTP_404_NOT_FOUND)


class HighestRatedProduct(APIView):
    def get(self, request):
        highest_rated_products = Product.objects.annotate(
            avg_rating=Avg('products__rating')
        ).filter(is_active=True, is_delete=False).order_by('-avg_rating')[:2]

        if highest_rated_products.exists():
            highest_rated_products_serializer = ProductSerializer(highest_rated_products, many=True)
            return Response(highest_rated_products_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'No products found'}, status=status.HTTP_404_NOT_FOUND)


class BestSellingProduct(APIView):

    def get(self, request):
        best_selling_product = OrderDetail.objects.values('product').annotate(
            total_sell=Sum('count')
        ).filter(order__status='paid').order_by('-total_sell')[:10]

        product_ids = [item['product'] for item in best_selling_product]
        best_selling_product = Product.objects.filter(id__in=product_ids, is_active=True, is_delete=False)

        if best_selling_product.exists():
            best_selling_product_serializer = ProductSerializer(best_selling_product, many=True)
            return Response(best_selling_product_serializer.data, status=status.HTTP_200_OK)
        return Response({'msg': 'No products found'}, status=status.HTTP_404_NOT_FOUN)

class TheNewestProduct(APIView):

    def get(self, request):
        new_product = Product.objects.filter(date_register__lte=datetime.date.today(),
                                             is_active=True, is_delete=False).order_by('-date_register')[:10]

        if new_product.exists():
            new_product_serializer = ProductSerializer(new_product, many=True)
            return Response(new_product_serializer.data, status=status.HTTP_200_OK)
        return Response({'msg': 'No products found'}, status=status.HTTP_404_NOT_FOUN)

class TheOldestProduct(APIView):

    def get(self, request):
        old_product = Product.objects.filter(date_register__lt=datetime.date.today(),
                                             is_delete=False, is_active=True).order_by('date_register')[:10]

        if old_product.exists():
            old_product_serializer = ProductSerializer(old_product, many=True)
            return Response(old_product_serializer.data, status=status.HTTP_200_OK)
        return Response({'msg': 'No products found'}, status=status.HTTP_404_NOT_FOUN)