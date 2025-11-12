from rest_framework import serializers

from categories.models import Category

class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={'blank': 'El nombre de la categoria no puede estar vacio'}
    )
    description = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={'blank': 'la descripcion de la categoria no puede estar vacio'}
    )
    file = serializers.ImageField(source='image', required=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'file']