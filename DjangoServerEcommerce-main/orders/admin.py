from django.contrib import admin
from orders.models import Order, OrderHasProducts

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_user', 'id_address', 'status', 'created_at')
    search_fields = ('status',)
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(OrderHasProducts)
class OrderHasProductsAdmin(admin.ModelAdmin):
    list_display = ('id_order', 'id_product', 'quantity', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
