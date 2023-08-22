from django.urls import path, include
from .views import ProductCategoryView, ProductView, GetProductByCategory, RatingProductView,\
    RatingProductByUserAndAdmin, RatingProductByAdmin, AllOfCommentForAdmin, ShortProductInformationView, \
    CommentRatingForShortInfoView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductView, basename='product')

urlpatterns = [
    path('category-register/', ProductCategoryView.as_view(), name='category-register'),
    path('products/<int:pk>/category/', GetProductByCategory.as_view(), name='product-by-category'),
    path('products/<int:pk>/rating/', RatingProductView.as_view({'post': 'create'}), name='product-rating'),
    path('products/<int:pk>/rating-product/', RatingProductByUserAndAdmin.as_view({'get': 'list'}),
         name='product-rating-by-admin-and-user'),
    path('products/rating-product/<int:pk>/', RatingProductByAdmin.as_view({'get': 'list', 'patch': 'partial_update',
                                                                            'delete': 'destroy'}),
         name='product-rating-by-admin'),

    path('products/all-rating/', AllOfCommentForAdmin.as_view(), name='all-rating'),
    path('products/short-info/<int:pk>/', ShortProductInformationView.as_view({'get': 'list'}), name='short-info'),
    path('products/short-comment-info/<int:pk>/', CommentRatingForShortInfoView.as_view({'get': 'list'}),
         name='short-comment-info'),
    path('', include(router.urls)),
]

