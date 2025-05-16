from rest_framework import serializers
from .models import Quotes
from rfpDetails.models import RFP
from vendor.models import Vendor

class QuoteCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Quotes
        fields = [
                  'vendors_price',
                  'quantity',
                  'item_description',   
                  'total_cost']



class QuoteListSerializer(serializers.ModelSerializer):
    vendor_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    item_price = serializers.IntegerField(source='vendors_price')

    class Meta:
        model = Quotes
        fields = [
            'vendor_id',
            'name',
            'item_price',
            'quantity',
            'total_cost',
            'email',
            'mobile'
        ]

    def get_vendor_id(self, obj):
        return obj.vendor.id

    def get_name(self, obj):
        return obj.rfp.title

    def get_email(self, obj):
        return obj.vendor.user.email

    def get_mobile(self, obj):
        return obj.vendor.phone_no
