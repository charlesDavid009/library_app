from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from rest_framework import serializers
from  .models import MyUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(label = "password")
    password2 = serializers.CharField(label = "confirm password")
    class Meta:
        model = MyUser
        fields = ["first_name", "last_name", "email", "username", "date_of_birth", "password1", "password2"]
        extra_kwargs = {"password1": {"write_only": True}, "password2": {"write_only": True}}

    def validate(self, data ):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Paawords doesn't match")
        username = '@' + data['username']
        return data

    def create(self, validated_data):
        tag = ("@")
        username = tag + validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        date_of_birth = validated_data['date_of_birth']
        password = validated_data['password1']
        user_obj = MyUser.objects.create_user(username = username,
                        email = email,
                        first_name = first_name,
                        last_name = last_name,
                        date_of_birth = date_of_birth
                        )
        user_obj.set_password(password)
        print(user_obj)
        user_obj.save()
        return user_obj

class LoginSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        username = '@'+ obj['username']
        user = MyUser.objects.get(username=username)

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    class Meta:
        model= MyUser
        fields = ['username', 'password', 'token']
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user_obj = None
        token = None
        tag = ("@")
        password = data['password']
        username= tag + data['username']
        user = MyUser.objects.filter(username= username)
        if user.exists():
            user_obj = user.first()
            if not user_obj.is_active:
                    raise AuthenticationFailed('Account disabled, contact admin')
            if not user_obj.is_verified:
                raise AuthenticationFailed('Email is not verified')
        else:
            raise AuthenticationFailed('Invalid credentials, try again')
        if user_obj:
            if not user_obj.check_password(password):
                raise AuthenticationFailed('Invalid credentials, try again')
        return {
            'email': user_obj.email,
            'username': user_obj.username,
            'tokens': user_obj.token
        }

class UserInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['username', 'full_name']

    def get_full_name(self, obj):
        full_name = obj.first_name + " " + obj.last_name
        return full_name




class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

"""
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)
"""

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField( min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = MyUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
