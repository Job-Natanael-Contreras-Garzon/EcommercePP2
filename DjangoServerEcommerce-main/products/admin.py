from django.contrib import admin
from products.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'id_category', 'created_at')
    search_fields = ('name',)
    list_filter = ('id_category', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
