from .serializers import RegisterUserSerializer, ChangePasswordSerializer, \
    SendRestLinkPasswordSerializer, RestPasswordSerializer, LoginSerializer, ProfileSerializer, ProfileUpdateSerializer
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import Util
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Profile
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import CanEditAndRegisterProfile
from rest_framework.decorators import action

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class RegisterUserView(APIView):

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            verification_link = request.build_absolute_uri(f'http://127.0.0.1:8000/user/verify-email/{uid}/{token}/')
            body = 'click following the link ' + verification_link

            data = {
                'subject': 'activate your email',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailActiveLink(APIView):

    def get(self, request, uid, token):
        try:
            id = urlsafe_base64_decode(force_str(uid))
            user = User.objects.get(id=id)
        except(TypeError, ValueError ,OverflowError, User.DoesNotExist):
            return Response({'msg': 'token invalid'}, status=status.HTTP_404_NOT_FOUND)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponseRedirect(reverse('success'))
        return Response({'error': 'Invalid Token'}, status=status.HTTP_404_NOT_FOUND)


class SuccessPageView(APIView):
    def get(self, request):
        return Response({'msg': 'validation successful!'})


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(
                request,
                username=username,
                password=password
            )
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'login successful'}, status=status.HTTP_200_OK)
            return Response({'error': 'login failed'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            return Response({'msg': 'your password changed'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendRestLinkPasswordView(APIView):

    def post(self, request):
        serializer = SendRestLinkPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'msg': 'email for rest password send!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestPasswordView(APIView):

    def post(self, request, uid, token):
        serializer = RestPasswordSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid():
            return Response({'msg': 'your password rest!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileUser(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        profile = self.queryset.filter(user=user)
        return profile
    def get_serializer_class(self):
        if self.action == 'update':
            return ProfileUpdateSerializer
        return self.serializer_class
    def get_permissions(self):
        if self.action == 'update':
            permission_classes = [CanEditAndRegisterProfile]
        elif self.action == 'create':
            permission_classes = [CanEditAndRegisterProfile]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        profile_id = self.kwargs.get('pk')
        profile = Profile.objects.get(pk=profile_id)
        if profile:
            profile.delete()
            return Response({'msg': 'user deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'profile not found'}, status=status.HTTP_404_NOT_FOUND)

