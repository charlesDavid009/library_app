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
        user_obj.save()
        return validated_data

class LoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank= True, read_only= True)
    class Meta:
        model= User
        fields = ['username', 'password', 'token']
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user_obj = None
        tag = ("@")
        password = data['password']
        username= tag + data['username']
        user = User.objects.filter(username= username)
        if user.exists():
            user_obj = user.first()
            print(user_obj)
        else:
            raise ValidationError("Invalid Credentials Username")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError('Invalid password')
        data['token']= 'SOME RANDOM TOKEN'
        return data
