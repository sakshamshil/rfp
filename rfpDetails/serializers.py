from rest_framework import serializers
from .models import RFP
from category.models import Categories
from vendor.models import Vendor


class VendorUserPKRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Vendor.objects.all()

    def to_internal_value(self, data):
        try:
            # Look up Vendor by user_id
            return Vendor.objects.get(user__id=data)
        except Vendor.DoesNotExist:
            raise serializers.ValidationError(
                f"Vendor with user id {data} does not exist."
            )

class RFPCreateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all(), many=True)
    vendors = VendorUserPKRelatedField(many=True)

    class Meta:
        model = RFP
        fields = [
            'title', 'rfp_no', 'quantity', 'last_date',
            'minimum_price', 'maximum_price', 'categories',
            'vendors', 'item_description'
        ]

    def validate(self, data):
        categories = data.get('categories')
        vendors = data.get('vendors')

        rfp_category_ids = set(cat.id for cat in categories)

        for vendor in vendors:
            vendor_category_ids = set(cat.id for cat in vendor.categories.all())
            if not vendor_category_ids & rfp_category_ids:
                raise serializers.ValidationError(
                    f"Vendor user ID:{vendor.user.id} does not belong to any of the RFP's categories."
                )

        return data

    # def validate(self, data):
    #     """
    #     This validate functions validate that the given vendors only belong to the given category
    #     """
    #     categories = data.get('categories')
    #     vendors = data.get('vendors')

    #     rfp_categories = set(categories)

    #     for vendor in vendors:
    #         vendor_categories = set(vendor.categories.all())

    #         #Intersection of both sets
    #         if not vendor_categories & rfp_categories:
    #             raise serializers.ValidationError(
    #                 f"Vendor ID:{vendor.id} does not belong to any of the RFP's categories."
    #             )

    #     return data
    
    # def validate(self, data):
    #     categories = data.get('categories')
    #     vendors = data.get('vendors')

    #     rfp_category_ids = set(cat.id for cat in categories)
    #     print(rfp_category_ids)

    #     for vendor in vendors:
    #         vendor_category_ids = set(cat.id for cat in vendor.categories.all())
    #         print (vendor_category_ids)

    #         if not vendor_category_ids & rfp_category_ids:
    #             raise serializers.ValidationError(
    #                 f"Vendor ID:{vendor.user.id} does not belong to any of the RFP's categories."
    #             )

    #     return data

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
        fields = ['id', 'title', 'rfp_no', 'quantity', 'last_date',
                  'minimum_price', 'maximum_price', 'categories',
                  'vendors', 'item_description', 'status']
        

