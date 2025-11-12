from rest_framework import serializers

from address.serializers import AddressSerializer
from orders.models import Order, OrderHasProducts
from products.serializers import ProductSerializer
from users.serializers import UserSerializer

class OrderHasProductsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(source='id_product')

    class Meta:
        model = OrderHasProducts
        fields = ['id_order', 'id_product', 'product', 'quantity', 'created_at', 'updated_at']

class OrderListSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='id_user')
    address = AddressSerializer(source='id_address')
    orderHasProducts = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'id_address', 'id_user', 'user', 'address', 'status', 'created_at', 'updated_at', 'orderHasProducts']

    def get_orderHasProducts(self, obj):
        order_has_products = OrderHasProducts.objects.filter(id_order=obj)
        return OrderHasProductsSerializer(order_has_products, many=True).data