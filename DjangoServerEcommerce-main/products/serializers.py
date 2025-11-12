from rest_framework import serializers

from categories.models import Category
from products.models import Product
from django.conf import settings


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages= {'blank': 'El nombre del producto no puede estar vacío.'}
    )
    description = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages= {'blank': 'La descripcion del producto no puede estar vacía.'}
    )
    price = serializers.FloatField(required=True)
    id_category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        error_messages = {'does_not_exist': 'La categoria no existe'}
    )
    image1 = serializers.SerializerMethodField()
    image2 = serializers.SerializerMethodField()

    class Meta:
        model= Product
        fields=['id', 'id_category', 'name', 'description', 'price', 'image1', 'image2', 'created_at', 'updated_at']

    def get_image1(self, obj):
        if obj.image1:
            return f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{obj.image1.url if hasattr(obj.image1, "url") else obj.image1}'
        return None

    def get_image2(self, obj):
        if obj.image2:
            return f'http://{settings.GLOBAL_IP}:{settings.GLOBAL_HOST}{obj.image2.url if hasattr(obj.image2, "url") else obj.image2}'
        return None