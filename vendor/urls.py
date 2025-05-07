from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('vendorlist/', VendorListView.as_view(), name = 'vendorlist'),
    path('vendorlist/<int:category_id>/', VendorByCategoryView.as_view(), name = 'vendor_category'),
    path('approveVendor/', ApproveVendorView.as_view(), name = 'approve_vendor'),
]