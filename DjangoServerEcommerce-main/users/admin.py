from django.contrib import admin
from users.models import User, UserHasRoles

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lastname', 'email', 'phone', 'created_at')
    search_fields = ('email', 'name', 'lastname')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserHasRoles)
class UserHasRolesAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_rol')
    list_filter = ('id_rol',)
