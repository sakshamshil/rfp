from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Categories
from rfp.permissions import IsAdmin
from rest_framework_simplejwt.authentication import JWTAuthentication


class CategoryView (APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request):
        """
        Return a list of all categories.
        """
        try : 
            categories = Categories.objects.all()
            serializer = CategorySerializer(categories, many=True)
            
            return Response({
                "response" : "success", 
                "categories" : serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e :
            return Response({
                "response" : "success", 
                "categories" : e
            }, status=status.HTTP_400_BAD_REQUEST)
        
    
    def post(self, request):
        """
        Add a new category by PUT call to the API
        """
        try:
            serializer = CategorySerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
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
        

class DeleteCategoryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request, category_id):
        """
        this function handles api call to delete a category using id
        """
        category = Categories.objects.filter(id = category_id)

        try:
            if category.exists():
                category.delete()
                return Response({
                "response": "success"
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'response': 'error',
                    'errors': 'Invalid ID'
                }, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({
                "response" : "success", 
                "categories" : e
            }, status=status.HTTP_400_BAD_REQUEST)
        

class CategoryByIDView (APIView):
    
    def get(self, request, category_id):
        """
        This function handles api call to update a category by its id
        """
        try:
            category = Categories.objects.get(id = category_id)
            serializer = CategorySerializer(category)
            return Response({
                "response": "success",
                "categories": serializer.data
            }, status=status.HTTP_200_OK)
        except Categories.DoesNotExist:
            return Response({
                "response": "error",
                "error" : "Invalid ID"
            }, status=status.HTTP_200_OK)
        
    def put(self, request, category_id):
        """
        This function handles api call to update a category by its id
        """
        try:
            category = Categories.objects.get(id = category_id)

            serializer = CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                if not name:
                    return Response({
                        "response": "error",
                        "error": "Name is required"
                        })
                
                else :
                    category.name = name
                    category.status = serializer.validated_data.get('status', category.status)
                    category.save()
                    return Response({
                        "response": "success"
                    }, status=status.HTTP_200_OK)
                
            else:
                return Response({
                "response" : "success", 
                "categories" : serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

            
        except Categories.DoesNotExist:
            return Response({
                "response": "error",
                "error" : "Invalid ID"
            }, status=status.HTTP_200_OK)
        
    