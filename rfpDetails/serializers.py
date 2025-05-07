from rest_framework import serializers
from .models import RFP
from category.models import Categories
from vendor.models import Vendor

class RFPCreateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all(), many=True)
    vendors = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all(), many=True)

    class Meta:
        model = RFP
        fields = ['title', 'rfp_no', 'quantity', 'last_date',
                  'minimum_price', 'maximum_price', 'categories',
                  'vendors', 'item_description']

    def validate(self, data):
        """
        This validate functions validate that the given vendors only belong to the given category
        """
        categories = data.get('categories')
        vendors = data.get('vendors')

        rfp_categories = set(categories)

        for vendor in vendors:
            vendor_categories = set(vendor.categories.all())

            #Intersection of both sets
            if not vendor_categories & rfp_categories:
                raise serializers.ValidationError(
                    f"Vendor ID:{vendor.id} does not belong to any of the RFP's categories."
                )

        return data

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        vendors = validated_data.pop('vendors', [])
        rfp = RFP.objects.create(**validated_data)
        rfp.categories.set(categories)
        rfp.vendors.set(vendors)
        return rfp



class RFPListSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    vendors = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = RFP
        fields = ['title', 'rfp_no', 'quantity', 'last_date',
                  'minimum_price', 'maximum_price', 'categories',
                  'vendors', 'item_description', 'status']
        

