import datetime
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from .models import Order, OrderDetail, RegisterOrder
from product_app.models import Product
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ProductToOrderSerializers, OrderSerializer, RegisterOrderSerializer
from rest_framework.decorators import action
from user_app.permissions import CanRegisterOrder, IsAdminUser
from user_app.models import Profile, User

class AddProductToBasket(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        user = self.request.user

        product_id = request.data.get('product_id')
        count = int(request.data.get('count', 0))
        if count < 1:
            return Response({'msg': "count can't be negative"}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_authenticated:
            product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
            if product is not None:

                current_order, created = Order.objects.get_or_create(status='no_paid', user_id=user.id)
                current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
                if current_order_detail is not None:
                    current_order_detail.count += count
                    current_order_detail.save()
                else:
                    new_order_detail = OrderDetail(order_id=current_order.id, count=count, product_id=product_id)
                    new_order_detail.save()
                return Response({'msg': 'محصول به سبد خرید افزوده شد'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({'msg': "not authorize"}, status=status.HTTP_401_UNAUTHORIZED)

class BasketView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        user = request.user
        current_order = Order.objects.filter(status='no_paid', user=user).first()
        final_price = 0
        order_detail_all = []
        if current_order:
            order_detail = current_order.orderdetail_set.all()
            for detail in order_detail:

                final_price += detail.product.price * detail.count
                detail.final_price = final_price

                order_detail_all.append(detail)
            serializer = ProductToOrderSerializers(order_detail_all, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'msg': 'سبد خرید خالی است'}, status=status.HTTP_200_OK)


class BasketOptionView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, pk):
        user = request.user

        current_order = Order.objects.prefetch_related('orderdetail_set').filter(status='no_paid', user=user, id=pk)

        if current_order:
            current_order.delete()
            return Response({'msg': 'سبد خرید با موفقیت پاک شد'}, status=status.HTTP_200_OK)
        return Response({'msg': 'سبد خرید خالی است'}, status=status.HTTP_200_OK)

    def put(self, request, pk):

        user = request.user
        product_id = request.data.get('product_id')
        new_count = int(request.data.get('count'))
        try:
            current_order = Order.objects.get(user=user, status='no_paid', id=pk)
        except Order.DoesNotExist:
            return Response({'msg': 'سبد خرید خالی است'}, status=status.HTTP_200_OK)

        if current_order:
            detail_order_to_update = current_order.orderdetail_set.filter(product_id=product_id)

            if detail_order_to_update:

                order_detail_objects = current_order.orderdetail_set.all()
                final_price_obj = 0
                order_detail_all = []
                for detail in order_detail_objects:
                    detail.count = new_count
                    final_price_obj += detail.product.price * detail.count
                    detail.final_price = final_price_obj
                    order_detail_all.append(detail)
                serializer = ProductToOrderSerializers(order_detail_all, many=True)

                return Response({'msg': 'order detail is updated', 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'جزئیات مورد نظر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

class ChangeStatusOrderAfterPayment(viewsets.ModelViewSet):

    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    @action(detail=True, methods=['post'])
    def make_payment(self, request):
        user = request.user
        order = Order.objects.filter(status='no_paid', user=user).last()
        if order:

            order.payment_date = timezone.now().date()
            order.status = 'paid'
            order.save()
            return Response({'mag': 'Payment has been made successfully'},
                            status=status.HTTP_200_OK)
        return Response({'msg': 'No pending order found for payment'},
                        status=status.HTTP_400_BAD_REQUEST)


class RegisterOrderView(viewsets.ModelViewSet):


    serializer_class = RegisterOrderSerializer
    queryset = RegisterOrder.objects.all()
    permission_classes = [CanRegisterOrder]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [CanRegisterOrder]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        try:
            profile = request.user.profile.id
        except Profile.DoesNotExist:
            return Response({'msg': 'profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

        request.data['user_profile'] = request.user.profile.id
        serializer = RegisterOrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        if queryset:
            serializer = RegisterOrderSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({'msg': 'not'}, status=status.HTTP_200_OK)


class RegisterOrderByAdmin(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            profile = user.profile
        except User.DoesNotExist:
            return Response({'msg': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Profile.DoesNotExist:
            return Response({'msg': 'Profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

        queryset = RegisterOrder.objects.filter(user_profile=profile)
        serializer = RegisterOrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
