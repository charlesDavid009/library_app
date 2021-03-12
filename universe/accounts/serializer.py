from rest_framework import serializers
from .models import Users

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}, 'confirm' : {'write_only' : True}}

    def validate(self, attrs):
        """
        VALIDATING NEW USER INFORMATION
        """
        email = attrs.get('email')
        if Users.objects.filter(email= email).exists():
            raise serializers.ValidationError({'dteials' : 'This email already exists!!'})
        if attrs.get('password') != attrs.get('confirm'):
            raise serializers.ValidationError({"Details": "Those passwords doesn't match"})
        return attrs

    def create(self, validated_data):
        """
        CREATING NEW USERS
        """
        new_tag = ('@')
        new_user = Users.objects.create(
            first_name= validated_data['first_name'], last_name= validated_data['first_name'],
            username = new_tag + validated_data['username'], email= validated_data['email'],
            password =validated_data['password'])
        return new_user

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

    class Meta:
        model = Users
        fields = 'username', 'password'
        extra_kwargs = {'password': {'write_only': True}}
