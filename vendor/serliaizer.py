from rest_framework import serializers
from .models import Vendor
from category.models import Categories

class VendorSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = ['user_id', 'name', 'email', 'phone_no', 'no_of_employees', 'approval']

    def get_user_id(self, obj):
        return obj.user.id

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_email(self, obj):
        return obj.user.email
    
    

class VendorByCategorySerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    categories = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Vendor
        fields = ['user_id', 'name', 'email', 'no_of_employees', 'approval', 'categories']

    def get_user_id(self, obj):
        return obj.user.id

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_email(self, obj):
        return obj.user.email
    


class ApproveVendorSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    approval = serializers.ChoiceField(choices=['approved', 'pending', 'rejected'])