from django.urls import path
from .views import GlobalSearch_dynamic, cheapestProduct, expensiveProduct, HighestRatedProduct, BestSellingProduct, \
    TheNewestProduct, TheOldestProduct

urlpatterns = [
    path('search/', GlobalSearch_dynamic.as_view(), name='search'),
    path('cheap-product/', cheapestProduct.as_view(), name='cheap-product'),
    path('expensive-product/', expensiveProduct.as_view(), name='expensive-product'),
    path('highest-rated-product/', HighestRatedProduct.as_view(), name='highest-rated-product'),
    path('best-sell-product/', BestSellingProduct.as_view(), name='best-sell-product'),
    path('the-new-product/', TheNewestProduct.as_view(), name='the-new-product'),
    path('the-old-product/', TheOldestProduct.as_view(), name='the-old-product'),
]