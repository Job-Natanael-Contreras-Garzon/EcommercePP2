from rest_framework import serializers

from address.models import Address
from users.models import User

class AddressSerializer(serializers.ModelSerializer):
    address = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={'blank': 'La direccion no puede estar vacia'}
    )
    neighborhood = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={'blank': 'El barrio no puede estar vacia'}
    )
    id_user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        error_messages = {'does_not_exist': 'El usuario no existe'}
    )
    class Meta:
        model = Address
        fields = ['id', 'id_user', 'address', 'neighborhood', 'created_at', 'updated_at']