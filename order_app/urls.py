from django.urls import path
from .views import AddProductToBasket, BasketView, BasketOptionView, ChangeStatusOrderAfterPayment

change_status_order = ChangeStatusOrderAfterPayment.as_view({
    'post': 'make_payment',
})


urlpatterns = [
    path('add-product-to-order/', AddProductToBasket.as_view(), name='add-product-to-order'),
    path('product-to-order/', BasketView.as_view(), name='product-to-order'),
    path('product-to-order-action/<int:pk>/', BasketOptionView.as_view(), name='product-to-order-action'),
    path('change-status-order-payment/', change_status_order,
         name='change-status-order-payment'),


]
