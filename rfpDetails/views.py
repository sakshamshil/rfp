from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rfp.permissions import IsAdmin
from rest_framework.response import Response
from rest_framework import status
from .models import RFP
from users.models import User
from rfp.utils import send_simple_message

class RFPListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    

    def get(self, request):
        """
        To get the details of all RFPs
        """
        try:
            rfp = RFP.objects.all()
            if rfp.exists():
                serializer = RFPListSerializer(instance=rfp, many=True)
                return Response({
                    "message" : "success",
                    "rfp" : serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message" : "No RFP exists"
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "error",
                "error": str(e)
            }, status=status.HTTP_404_NOT_FOUND)


class RFPCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def post(self, request):
        """
        API Call to create a new RFP & send email to targeted vendors
        """
        try:
            serializer = RFPCreateSerializer(data=request.data)
            if serializer.is_valid():
                rfp = serializer.save()

                #Send email to all targeted vendors
                vendors = rfp.vendors.all()
                for vendor in vendors:
                    if vendor.approval == 'approved':
                        to_email = vendor.user.email
                        to_name = f"{vendor.user.first_name} {vendor.user.last_name}"
                        subject = f"New RFP Opportunity: {rfp.title}"
                        message = f"Hello {to_name},\n\nYou have been invited to submit a quote for a new RFP: '{rfp.title}'.\n\nPlease log in to view details and submit your bid {rfp.last_date}.\n\nThank you."
                        send_simple_message(to_email, to_name, subject, message)

                return Response({"response": "success"}, status=status.HTTP_200_OK)

            return Response({
                'response': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "response": "error",
                "errors": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)




class RFPDetailsView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    

    def put(self, request, id):
        """
        To get the RFP details by rfp_id
        """
        rfp_id = id
        try:
            rfp = RFP.objects.get(id=rfp_id)
            serializer = RFPListSerializer(instance=rfp)
            return Response({
                "message" : "success",
                "rfp" : serializer.data
            }, status=status.HTTP_200_OK)
        except RFP.DoesNotExist:
            return Response({
                "message": "error",
                "error": "RFP ID does not exist"
            }, status=status.HTTP_404_NOT_FOUND)
        

    def get(self, request, id):
        user_id = id
        try:
            user = User.objects.get(id = user_id)
            vendor = Vendor.objects.get(user=user)
        except User.DoesNotExist:
            return Response({
                "response": "error",
                "error": "User does not exist"
                }, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({
                "response": "error",
                "error": "User is not a vendor"
                }, status=status.HTTP_200_OK)
        try:
            rfp = RFP.objects.filter(vendors = vendor)
            serializer = RFPListSerializer(instance=rfp, many = True)
            return Response({
                "message" : "success",
                "rfp" : serializer.data
            }, status=status.HTTP_200_OK)
        except RFP.DoesNotExist:
            return Response({
                "message": "error",
                "error": "RFP ID does not exist"
            }, status=status.HTTP_404_NOT_FOUND)


class CloseRFPView (APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]


    def put(self, request, rfp_id):
        """
        To close the RFP
        """
        try:
            rfp = RFP.objects.get(id=rfp_id)
            rfp.status = "close"
            rfp.save()
            return Response({
                "message" : "success",
                "quotes" : "RFP closed"
            }, status=status.HTTP_200_OK)
        except RFP.DoesNotExist:
            return Response({
                "message": "error",
                "error": "RFP ID does not exist"
            }, status=status.HTTP_404_NOT_FOUND)



class UpdateRFPView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def put(self, request):
        """
        This API is responsible for updating the RFP        
        """
        rfp_id = request.data.get('rfp_id')

        if not rfp_id:
            return Response({
                "message": "error",
                "error": "RFP ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            rfp = RFP.objects.get(id=rfp_id)
            if rfp.status == "close":
                return Response({
                    "response": "error",
                    "errors": "RFP is closed"
                    }, status=status.HTTP_200_OK)
        except RFP.DoesNotExist:
            return Response({
                "message": "error",
                "error": "RFP ID does not exist"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = RFPCreateSerializer(instance=rfp, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "success"
            }, status=status.HTTP_200_OK)

        else :
            return Response({
                "message": "error",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)