from rest_framework import serializers
from .models import Categories


class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name', 'status']


    def get_status_display(self, obj):
        return obj.get_status_display()