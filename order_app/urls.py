from django.urls import path, include
from .views import AddProductToBasket, BasketView, BasketOptionView, ChangeStatusOrderAfterPayment, RegisterOrderView, RegisterOrderByAdmin
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('register-order', RegisterOrderView, basename='register-order')

change_status_order = ChangeStatusOrderAfterPayment.as_view({
    'post': 'make_payment',
})


urlpatterns = [
    path('add-product-to-order/', AddProductToBasket.as_view(), name='add-product-to-order'),
    path('product-to-order/', BasketView.as_view(), name='product-to-order'),
    path('product-to-order-action/<int:pk>/', BasketOptionView.as_view(), name='product-to-order-action'),
    path('change-status-order-payment/', change_status_order,
         name='change-status-order-payment'),
    path('get-by-admin-order/<int:pk>/', RegisterOrderByAdmin.as_view(), name='get-by-admin-order'),
    path('', include(router.urls))


]
