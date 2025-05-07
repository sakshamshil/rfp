from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name = 'login'),
    path('registeradmin/', SignupAdminView.as_view(), name = 'register_admin'),
    path('registervendor/', SignupVendorView.as_view(), name = 'register_vendor'),
    path('resetPassword/', ResetPasswordView.as_view(), name = 'reset_password'),
]
