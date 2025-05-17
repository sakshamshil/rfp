from django.shortcuts import render
from rfp.permissions import IsVendor, IsAdmin
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rfpDetails.models import RFP
from vendor.models import Vendor
from rfp.utils import send_simple_message
from users.models import User

class ApplyRFPView (APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsVendor]


    def post (self, request, rfp_id):
        try:
            rfp = RFP.objects.get(id=rfp_id)
        except RFP.DoesNotExist:
            return Response({
                "response": "error",
                "message": "Invalid RFP ID"
            }, status=status.HTTP_200_OK)
        
        user = request.user
        try:
            vendor = Vendor.objects.get(user=user)
        except Vendor.DoesNotExist:
            return Response({
                "response": "error",
                "message": "Vendor not found"
            }, status=status.HTTP_200_OK)
        
        if vendor not in rfp.vendors.all():
            return Response({
                "response": "error",
                "message": "Action not allowed"
            }, status=status.HTTP_200_OK)
        
        quote = Quotes.objects.filter(rfp=rfp, vendor=vendor)
        if quote.exists():
            return Response({
                "response": "error",
                "message": "You already applied"
            }, status=status.HTTP_200_OK)
        
        

        try:
            serializer = QuoteCreateSerializer(data=request.data)

            if serializer.is_valid():
                Quotes.objects.create(rfp=rfp, vendor=vendor, **serializer.validated_data)

                #Send email to all admins
                admins = User.objects.filter(user_type='admin')
                
#                 for admin in admins:
#                     to_email = admin.email
#                     to_name = f"{admin.first_name} {admin.last_name}"
#                     subject = f"A Bid have been submitted for {rfp.title}"
#                     message = f"""
# Hi Admin {to_name},

# Vendor "{user.first_name} {user.last_name}" has submitted a quote for the RFP titled "{rfp.title}".

# Details of the submitted quote:
# - Quote Price: Rs. {serializer.validated_data['total_cost']}
# - Quantity: {serializer.validated_data['quantity']}

# Thanks,  
# Velocity RFP System"""
                    
#                     send_simple_message(to_email, to_name, subject, message)


                return Response({
                "response": "success"
                }, status=status.HTTP_200_OK)
            
            else :
                return Response({
                    'response': 'error',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e :
            return Response({
                "response" : "error", 
                "errors" : str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        


class QuotesListView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes  = [IsAdmin]

    def get(self, request, rfp_id):
        try:
            rfp = RFP.objects.get(id=rfp_id)
        except RFP.DoesNotExist:
            return Response({
                "response": "error",
                "message": "Invalid RFP ID"
            }, status=status.HTTP_200_OK)
        
        quotes = Quotes.objects.filter(rfp=rfp)
        
        if not quotes.exists():
            return Response({
                "response": "error",
                "error": "No quotes available"
            }, status=status.HTTP_200_OK)
        
        try:
            serializer = QuoteListSerializer(instance = quotes, many = True)
            return Response({
                "response": "success",
                "quotes": serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "response" : "error", 
                "errors" : str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        



class ListAllQuotesView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes  = [IsAdmin]

    def get(self, request):
        quotes = Quotes.objects.all()
        
        if not quotes.exists():
            return Response({
                "response": "error",
                "error": "No quotes available"
            }, status=status.HTTP_200_OK)
        
        try:
            serializer = QuoteListSerializer(instance = quotes, many = True)
            return Response({
                "response": "success",
                "quotes": serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "response" : "error", 
                "errors" : str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        