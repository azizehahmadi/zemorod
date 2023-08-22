from django.urls import path, include
from .views import RegisterUserView, EmailActiveLink, SuccessPageView, \
    LoginView, ChangePasswordView, SendRestLinkPasswordView, RestPasswordView, ProfileUser

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('profile', ProfileUser, basename='profile')

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/<str:uid>/<str:token>/', EmailActiveLink.as_view(), name='verify-email'),
    path('success/', SuccessPageView.as_view(), name='success'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('send-password-link/', SendRestLinkPasswordView.as_view(), name='send-password-link'),
    path('rest-password/<str:uid>/<str:token>/', RestPasswordView.as_view(), name='rest-password'),


    path('', include(router.urls))
]
