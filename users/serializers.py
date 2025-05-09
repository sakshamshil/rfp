from rest_framework import serializers
from .models import User
from vendor.models import Vendor    
from category.models import Categories
from django.db import transaction



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)



class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']  # Don't include 'user_type'

    def create(self, validated_data):
        password = validated_data['password']
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    

class VendorSignupSerialiser (serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    categories = serializers.PrimaryKeyRelatedField(
        queryset = Categories.objects.all(), 
        many = True
    )

    class Meta :
        model = Vendor
        fields = [
            'email', 'password', 'first_name', 'last_name',
            'categories', 'revenue', 'no_of_employees',
            'gst_no', 'pan_no', 'phone_no'
        ]
    
    def create(self, validated_data):
        with transaction.atomic():
            email = validated_data.pop('email')
            password = validated_data.pop('password')
            first_name = validated_data.pop('first_name')
            last_name = validated_data.pop('last_name')

            user = User(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type='vendor'
            )
            user.set_password(password)
            user.save()

            categories_data = validated_data.pop('categories')
            vendor = Vendor.objects.create(user=user, **validated_data)
            vendor.categories.set(categories_data)

        return vendor
    


class ResetPasswordSerializer (serializers.Serializer):
    email = serializers.EmailField()
    old_password = serializers.CharField(max_length = 128)
    new_password = serializers.CharField(max_length = 128)
