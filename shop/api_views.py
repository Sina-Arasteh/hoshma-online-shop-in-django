# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from . import models, serializers
# from django.http import Http404
# from .permissions import IsAdminOrReadOnly


# class CategoryListAPIView(APIView):
#     permission_classes = [IsAdminOrReadOnly]

#     def get(self, request):
#         categories = models.Category.objects.all()
#         serializer = serializers.CategorySerializer(categories, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = serializers.CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CategoryDetailAPIView(APIView):
#     permission_classes = [IsAdminOrReadOnly]

#     def get_object(self, pk):
#         try:
#             return models.Category.objects.get(pk=pk)
#         except models.Category.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         category = self.get_object(pk)
#         serializer = serializers.CategorySerializer(category)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         category = self.get_object(pk)
#         serializer = serializers.CategorySerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def patch(self, request, pk):
#         category = self.get_object(pk)
#         serializer = serializers.CategorySerializer(category, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         category = self.get_object(pk)
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class DiscountListAPIView(APIView):
#     permission_classes = [IsAdminOrReadOnly]

#     def get(self, request):
#         discounts = models.Discount.objects.all()
#         serializer = serializers.DiscountSerializer(discounts, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = serializers.DiscountSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DiscountDetailAPIView(APIView):
#     permission_classes = [IsAdminOrReadOnly]

#     def get_object(self, pk):
#         try:
#             return models.Discount.objects.get(pk=pk)
#         except models.Discount.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         discount = self.get_object(pk)
#         serializer = serializers.DiscountSerializer(discount)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         discount = self.get_object(pk)
#         serializer = serializers.DiscountSerializer(discount, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def patch(self, request, pk):
#         discount = self.get_object(pk)
#         serializer = serializers.DiscountSerializer(discount, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         discount = self.get_object(pk)
#         discount.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class TagListAPIView(APIView):
#     permission_classes = [IsAdminOrReadOnly]

#     def get(self, request):
#         tags = models.Tag.objects.all()
#         serializer = serializers.TagSerializer(tags, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = serializers.TagSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TagDetailAPIView(APIView):
#     permission_classes = [IsAdminOrReadOnly]

#     def get_object(self, pk):
#         try:
#             return models.Tag.objects.get(pk=pk)
#         except models.Tag.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         tag = self.get_object(pk)
#         serializer = serializers.TagSerializer(tag)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         tag = self.get_object(pk)
#         serializer = serializers.TagSerializer(tag, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         tag = self.get_object(pk)
#         tag.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ImageListAPIView(APIView):
#     permission_classes = [IsAdminOrReadOnly]

#     def get(self, request):
#         images = models.Image.objects.all()
#         serializer = serializers.ImageSerializer(images, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = serializers.ImageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ImageDetailAPIView(APIView):
#     permission_classes = [IsAdminOrReadOnly]

#     def get_object(self, pk):
#         try:
#             return models.Image.objects.get(pk=pk)
#         except models.Image.DoesNotExist:
#             raise Http404
    
#     def get(self, request, pk):
#         image = self.get_object(pk)
#         serializer = serializers.ImageSerializer(image)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         image = self.get_object(pk)
#         serializer = serializers.ImageSerializer(image, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def patch(self, request, pk):
#         image = self.get_object(pk)
#         serializer = serializers.ImageSerializer(image, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         image = self.get_object(pk)
#         image.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductListAPIView(APIView):
#     permission_classes = [IsAdminOrReadOnly]

#     def get(self, request):
#         products = models.Product.objects.all()
#         serializer = serializers.ProductSerializer(products, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = serializers.ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProductDetailAPIView(APIView):
#     permission_classes = [IsAdminOrReadOnly]

#     def get_object(self, pk):
#         try:
#             return models.Product.objects.get(pk=pk)
#         except models.Product.DoesNotExist:
#             raise Http404
    
#     def get(self, request, pk):
#         product = self.get_object(pk)
#         serializer = serializers.ProductSerializer(product)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         product = self.get_object(pk)
#         serializer = serializers.ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def patch(self, request, pk):
#         product = self.get_object(pk)
#         serializer = serializers.ProductSerializer(product, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         product = self.get_object(pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
