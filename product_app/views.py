from .serializers import ProductCategorySerializer, ProductSerializer, RatingProductSerializer, \
    ShortProductInformationSerializer, CommentRatingForShortInfoSerializer
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import ProductCategory, Product, RatingProduct
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from django.http import Http404
class ProductCategoryView(generics.ListCreateAPIView):

    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        else:
            return [AllowAny()]

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductView(viewsets.ModelViewSet):

    authentication_classes = [JWTAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class GetProductByCategory(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        category = self.kwargs['pk']
        return Product.objects.filter(category=category)


class RatingProductView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = RatingProductSerializer

    def create(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        product = Product.objects.filter(id=pk).first()
        user = self.request.user
        data = self.request.data.copy()
        data['user'] = user.id
        data['product'] = product.id
        data['ip'] = self.get_client_ip()
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_client_ip(self):
        x_forward_for = self.request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forward_for:
            ip = x_forward_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class RatingProductByUserAndAdmin(viewsets.GenericViewSet, mixins.ListModelMixin):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = RatingProductSerializer

    def list(self, request, *args, **kwargs):
        if self.request.user.is_admin:
            pk = self.kwargs['pk']
            product = Product.objects.filter(id=pk).first()
            if not product:
                return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

            rating = RatingProduct.objects.filter(product=product)
            serializer = self.get_serializer(rating, many=True)
            return Response(serializer.data)
        else:
            pk = self.kwargs['pk']
            product = Product.objects.filter(id=pk).first()
            if not product:
                return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            rating = RatingProduct.objects.filter(product=product, is_active=True, is_delete=False)
            serializer = self.get_serializer(rating, many=True)
            return Response(serializer.data)


class RatingProductByAdmin(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = RatingProductSerializer
    queryset = RatingProduct.objects.all()

    def list(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        rating = RatingProduct.objects.filter(id=pk)
        if not rating:
            return Response({'comment not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(rating, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):

        pk = self.kwargs['pk']
        if not RatingProduct.objects.filter(id=pk).exists():
            return Response({'msg': 'comment not found'}, status=status.HTTP_404_NOT_FOUND)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        rating = RatingProduct.objects.filter(id=pk).first()
        if not rating:
            return Response({'msg': 'comment not found'}, status=status.HTTP_404_NOT_FOUND)
        rating.delete()
        return Response({'comment deleted'}, status=status.HTTP_204_NO_CONTENT)


class AllOfCommentForAdmin(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = RatingProductSerializer
    queryset = RatingProduct.objects.all()


class ShortProductInformationView(viewsets.GenericViewSet, mixins.ListModelMixin):

    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    serializer_class = ShortProductInformationSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Product.objects.filter(id=pk)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({'msg': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ShortProductInformationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentRatingForShortInfoView(viewsets.GenericViewSet, mixins.ListModelMixin):

    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    serializer_class = CommentRatingForShortInfoSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return RatingProduct.objects.filter(product_id=pk, is_delete=False, is_active=True).all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CommentRatingForShortInfoSerializer(queryset, many=True)
        return Response(serializer.data)