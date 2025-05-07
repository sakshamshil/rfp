from django.shortcuts import render
from rest_framework.views import APIView
from .models import Vendor
from .serliaizer import *
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rfp.permissions import IsAdmin
from rest_framework.response import Response 
from rest_framework import status
from users.models import User


class VendorListView (APIView):
    """
    This view handles the api call to list all the vendors
    """
    
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAdmin]    

    def get(self, request):
        try:
            vendors = Vendor.objects.all()
            serializer = VendorSerializer(instance=vendors, many = True)
            return Response({
                "response" : "success",
                "vendors" : serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "response" : "error",
                "error" : e
            })


class VendorByCategoryView (APIView):
    """
    This view handles the api call to list all the vendors for a particular category
    """
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAdmin]    

    def get(self, request, category_id):
        if not Categories.objects.filter(id=category_id).exists():
            return Response({
                "response": "error",
                "error": "No category exist"
                }, status=status.HTTP_200_OK)
        
        
        try:
            vendors = Vendor.objects.filter(categories=category_id)
            if vendors.exists():
                serializer = VendorByCategorySerializer(instance=vendors, many = True)
                return Response({
                    "response" : "success",
                    "vendors" : serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "response" : "success",
                    "message" : "No vendors mapped with the category."
                }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "response" : "error",
                "error" : e
            })


class ApproveVendorView(APIView):
    """
    This view handles the put call to update a vendor's approval
    """
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAdmin]    

    def put(self, request):
        serializer = ApproveVendorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "response": "error",
                "errors": serializer.errors
            })

        user_id = serializer.validated_data['user_id']
        approval = serializer.validated_data['approval']       
         

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                "response": "error",
                "message": "User not exist"
            })

        try:
            vendor = Vendor.objects.get(user=user)
            vendor.approval = approval
            vendor.save()
        except Vendor.DoesNotExist:
            return Response({
                "response": "error",
                "message": "User not exist"
            })

        return Response({"response": "success"})