from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from vendor.models import Vendor
from rest_framework_simplejwt.authentication import JWTAuthentication


class LoginView(APIView):
    """
    This API handles the logic for a user login and returns an API Response
    """
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'response': 'error',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(email=email, password=password)


            # print(user)

            if user is None:
                return Response({
                    "response": "Error",
                    "error": "Invalid credentials"
                }, status=status.HTTP_200_OK)

            if user.user_type == 'vendor':
                try:
                    vendor = Vendor.objects.get(user=user)
                    if vendor.approval == 'pending':
                        return Response({
                            "response": "error",
                            "error": "Account status Pending"
                        }, status=status.HTTP_200_OK)
                    elif vendor.approval == 'rejected':
                        return Response({
                            "response": "error",
                            "error": "Account Rejected"
                        }, status=status.HTTP_200_OK)
                except Vendor.DoesNotExist:
                    return Response({
                        "response": "error",
                        "error": ["Vendor profile not found"]
                    }, status=status.HTTP_404_NOT_FOUND)

            refresh = RefreshToken.for_user(user)

            return Response({
                "response": "success",
                "user_id": user.id,
                "type": user.user_type,
                "name": f"{user.first_name} {user.last_name}",
                "email": user.email,
                "token": str(refresh.access_token)
            }, status=status.HTTP_200_OK)


        except Exception as e :
            return Response({
                "response" : "error", 
                "categories" : str(e)
            }, status=status.HTTP_400_BAD_REQUEST)



class SignupAdminView(APIView):
    """
    This API handles the logic for a admin singup 
    """


    def post(self, request):
        try:
            serializer = UserSignupSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'response': 'error',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            


            serializer.save()
            return Response({
                "response": "success"
            }, status=status.HTTP_200_OK)

        except Exception as e :
            return Response({
                "response" : "error", 
                "categories" : str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class SignupVendorView(APIView):
    """
    This API handles the logic for a vendor singup 
    """

    def post(self, request):
        try: 
            serializer = VendorSignupSerialiser(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'response': 'error',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                "response": "success"
            }, status=status.HTTP_200_OK)
        
        except Exception as e :
            return Response({
                "response" : "error", 
                "categories" : str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        


class ResetPasswordView(APIView):
    """
    This API view handles the reset password logic.
    """
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"response": "error", "error": "Enter valid email"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = authenticate(request, email=email, password=old_password)
            if user:
                user.set_password(new_password)
                user.save()
                return Response({"response": "success"}, status=status.HTTP_200_OK)

            return Response(
                    {"response": "error", "error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            

        
        else:
            return Response({
                    'response': 'error',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)