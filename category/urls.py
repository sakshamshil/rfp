from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('categories/', CategoryView.as_view(), name = 'category_list_add'),
    path('categories/delete/<int:category_id>/', DeleteCategoryView.as_view(), name = 'category_delete'),
    path('categories/<int:category_id>/', CategoryByIDView.as_view(), name = 'category_by_ID')
]