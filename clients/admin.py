from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('description', 'ethernet_ip', 'client_port', 'ethernet_status', 'wifi_status')
    list_filter = ('ethernet_status', 'wifi_status','created_at', 'updated_at')
    search_fields = ('description', 'ethernet_ip', 'client_port') 
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ()
    fieldsets = (
        ('Stable Fields', {
            'fields': ('user', 'ethernet_ip', 'client_port', 'client_username', 'client_password', 'client_lab', 'interface', 'description')
        }),
        ('Dynamic Fields', {
            'fields': ('ethernet_status', 'ssid_name', 'bssid', 'hwaddr', 'rssi', 'txpower', 'channel', 'channel_width', 'channel_band', 'security', 'phymode', 'phyrate', 'noise_measurement', 'wifi_status')
        }),
        ('Date Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) 
        }),
    )