from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os

from products.models import Product
from products.serializers import ProductSerializer


@api_view(['POST'])
@permission_classes([IsAdminUser])  # Solo ADMIN puede crear
def create(request):
    serializer = ProductSerializer(data=request.data)

    if not serializer.is_valid():
        error_messages = []
        for field, errors in serializer.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")

        error_response = {
            "message": error_messages,
            "statusCode": status.HTTP_400_BAD_REQUEST
        }

        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()

    uploaded_images = request.FILES.getlist('files')
    image_urls = []

    if uploaded_images:
        for index, image in enumerate(uploaded_images[:2]):
            file_path = f'uploads/products/{serializer.instance.id}/{image.name}'
            saved_path = default_storage.save(file_path, ContentFile(image.read()))
            image_urls.append(default_storage.url(saved_path))
        serializer.instance.image1 = image_urls[0] if len(image_urls) > 0 else None
        serializer.instance.image2 = image_urls[1] if len(image_urls) > 1 else None
        serializer.instance.save()

    product_data = ProductSerializer(serializer.instance).data
    return Response({
        **product_data,
        "image1": f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{serializer.instance.image1}' if serializer.instance.image1 else None,
        "image2": f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{serializer.instance.image2}' if serializer.instance.image2 else None,
    }, status=status.HTTP_201_CREATED)

   

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Todos pueden ver
def get_products_by_category(request, id_category):
    try:
        products = Product.objects.filter(id_category=id_category)
        if not products.exists():
            return Response({
                'message': 'No hay productos para esta categoria',
                'statusCode': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        serialized_products = []
        
        for product in products:
            serializer_data = ProductSerializer(product).data
            serializer_data['image1'] = f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{product.image1}' if product.image1 else None
            serializer_data['image2'] = f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{product.image2}' if product.image2 else None
            serialized_products.append(serializer_data)
        return Response(serialized_products, status=status.HTTP_200_OK)


    except Exception as e:
        return Response({
            'message': f'Error al obtener el producto: {str(e)}',
            'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
@permission_classes([IsAdminUser])  # Solo ADMIN puede eliminar
def delete(request, id_product):
    try:
        product = Product.objects.get(id=id_product)
        if product.image1:
            image1_path = product.image1.lstrip('/').replace('media/', '')
            full_path1 = os.path.join(settings.MEDIA_ROOT, image1_path)
            if default_storage.exists(full_path1):
                default_storage.delete(full_path1)
        
        if product.image2:
            image2_path = product.image2.lstrip('/').replace('media/', '')
            full_path2 = os.path.join(settings.MEDIA_ROOT, image2_path)
            if default_storage.exists(full_path2):
                default_storage.delete(full_path2)
        product.delete()

        return Response(True, status=status.HTTP_200_OK)

    except Product.DoesNotExist as e:
        return Response({
            'message': 'El producto no existe',
            'statusCode': status.HTTP_404_NOT_FOUND
        }, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
@permission_classes([IsAdminUser])  # Solo ADMIN puede editar
def update(request, id_product):
    try:
        product = Product.objects.get(id=id_product)
    except Product.DoesNotExist as e:
        return Response({
            'message': 'El producto no existe',
            'statusCode': status.HTTP_404_NOT_FOUND
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product, data=request.data, partial=True)
    
    if not serializer.is_valid():
        error_messages = []
        for field, errors in serializer.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")

        error_response = {
            "message": error_messages,
            "statusCode": status.HTTP_400_BAD_REQUEST
        }

        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()


    if 'files' in request.FILES:
        files = request.FILES.getlist('files')
        # ELIMINAR LAS IMAGENES
        
        if len(files) > 0:
            if product.image1:
                image1_path = product.image1.lstrip('/').replace('media/', '')
                full_path1 = os.path.join(settings.MEDIA_ROOT, image1_path)
                if default_storage.exists(full_path1):
                    default_storage.delete(full_path1)

            file_path1 = f'uploads/products/{product.id}/{files[0].name}'
            saved_path1 = default_storage.save(file_path1, ContentFile(files[0].read()))
            product.image1 = default_storage.url(saved_path1)

        if len(files) > 1:
            if product.image2:
                image2_path = product.image2.lstrip('/').replace('media/', '')
                full_path2 = os.path.join(settings.MEDIA_ROOT, image2_path)
                if default_storage.exists(full_path2):
                    default_storage.delete(full_path2)
            file_path2 = f'uploads/products/{product.id}/{files[1].name}'
            saved_path2 = default_storage.save(file_path2, ContentFile(files[1].read()))
            product.image2 = default_storage.url(saved_path2)

        product.save()
    
    serializer_data = ProductSerializer(product).data
    # serializer_data['image1'] = f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{product.image1}' if product.image1 else None
    # serializer_data['image2'] = f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{product.image2}' if product.image2 else None

    return Response(serializer_data, status=status.HTTP_200_OK)