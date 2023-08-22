from rest_framework import serializers
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User, Profile
import re
from .utils import Util
from django.contrib.auth.hashers import check_password


class RegisterUserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 12
            }
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('P1 and P2 not match!')
        return attrs

    def validate_email(self, value):
        if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", value):
            print(f"The email address {value} is not valid")
            raise serializers.ValidationError('the email address not valid!')
        if User.objects.filter(email__iexact=value).exists():
            return serializers.ValidationError('this email is already exist!')
        return value

    def validated_username(self, value):
        if not re.search(r"^[A-Za-z0-9_!#$%&'*+=?@]", value):
            print(f"The username {value} is not valid! should be (A-Za-z0-9_!#$%&'*+=?@)")
            raise serializers.ValidationError('The username is not valid!')
        if User.objects.filter(username__iexact=value).exists():
            return serializers.ValidationError('this username is already exist!')
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ('username', 'password')


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ('password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if password != password2:
            raise serializers.ValidationError('P1 and P2 not match!')
        user.set_password(password)
        user.save()
        return attrs


class SendRestLinkPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ('email',)

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email__iexact=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            link = 'http://127.0.0.1:8000/user/rest-password/' + uid + '/' + token

            # send email
            body = f'link ' + link
            data = {
                'subject': 'your rest password link',
                'body': body,
                'to_email': user.email

            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('email not found!')


class RestPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password2'}, write_only=True)

    class Meta:
        fields = ('password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        uid = self.context.get('uid')
        token = self.context.get('token')

        if password != password2:
            raise serializers.ValidationError('P1 and P2 not match!')

        id = urlsafe_base64_decode(force_str(uid))
        user = User.objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError('Token is not valid!')

        if check_password(password, user.password):
            raise serializers.ValidationError('New password should be different from the old password!')
        user.set_password(password)
        user.save()
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'role', 'shar', 'town', 'country', 'company', 'address',
                  'phone', 'code_post']

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user__username = serializers.ReadOnlyField(source='user.username')
    user__email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Profile
        fields = ['id', 'user', 'role', 'shar', 'town', 'country', 'company', 'address',
                  'phone', 'code_post', 'user__username', 'user__email']
