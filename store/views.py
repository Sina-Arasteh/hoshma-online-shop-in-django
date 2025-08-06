from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from django.http import Http404


class CategoryListAPIView(APIView):
    def get(self, request):
        categories = models.Category.objects.all()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return models.Category.objects.get(pk=pk)
        except models.Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = serializers.CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = serializers.CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DiscountListAPIView(APIView):
    def get(self, request):
        discounts = models.Discount.objects.all()
        serializer = serializers.DiscountSerializer(request.data)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiscountDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return models.Discount.objects.get(pk=pk)
        except models.Discount.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        discount = self.get_object(pk)
        serializer = serializers.DiscountSerializer(discount)
        return Response(serializer.data)

    def put(self, request, pk):
        discount = self.get_object(pk)
        serializer = serializers.DiscountSerializer(discount, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        discount = self.get_object(pk)
        discount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
