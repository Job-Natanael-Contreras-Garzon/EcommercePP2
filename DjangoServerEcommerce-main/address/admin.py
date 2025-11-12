from django.contrib import admin
from address.models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_user', 'address', 'neighborhood', 'created_at')
    search_fields = ('address', 'neighborhood')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
