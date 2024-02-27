from django.contrib import admin
from .models import Client

# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('name', 'user', 'created_at', 'updated_at')
#     search_fields = ('name', 'user__email')
#     list_filter = ('created_at', 'updated_at')
#     readonly_fields = ('created_at', 'updated_at')
#     filter_horizontal = ()

#     fieldsets = (
#         (None, {'fields': ('name', 'user', 'description')}),
#         ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
#     )

# @admin.register(Client)
# class ClientAdmin(admin.ModelAdmin):
#     list_display = ('clientName', 'group', 'clientIP', 'clientPort', 'created_at', 'updated_at')
#     search_fields = ('clientName', 'group__name')
#     list_filter = ('created_at', 'updated_at')
#     readonly_fields = ('created_at', 'updated_at')
#     filter_horizontal = ()

#     fieldsets = (
#         (None, {'fields': ('clientName', 'group')}),
#         ('Client Details', {'fields': ('clientIP', 'clientPort', 'clientUsername', 'clientPassword', 'clientLab', 'traffic_profile', 'description')}),
#         ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
#     )

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('clientName', 'user', 'clientIP', 'clientPort', 'created_at', 'updated_at')
    search_fields = ('clientName', 'user__name')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('clientName', 'group')}),
        ('Client Details', {'fields': ('clientIP', 'clientPort', 'clientUsername', 'clientPassword', 'clientLab', 'traffic_profile', 'description')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )