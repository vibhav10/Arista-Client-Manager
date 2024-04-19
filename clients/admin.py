from django.contrib import admin
from .models import Client



admin.site.site_header = "WiFi Agent Admin"
admin.site.site_title = "WiFi Agent Admin Portal"
admin.site.index_title = "Welcome to WiFi Agent Admin Portal"

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'description', 'ethernet_ip', 'client_port', 'ethernet_status', 'wifi_status')
    list_filter = ('ethernet_status', 'wifi_status','client_lab', 'created_at', 'updated_at')
    search_fields = ('description', 'ethernet_ip', 'user__email', 'client_lab', 'ssid_name', 'wifi_ip', 'hostname') 
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ()
    fieldsets = (
        ('Stable Fields', {
            'fields': ('user', 'hostname', 'ethernet_ip', 'client_port', 'client_username', 'client_password', 'client_lab', 'interface_name', 'description')
        }),
        ('Dynamic Fields', {
            'fields': ('ethernet_status', 'ssid_name', 'bssid', 'hwaddr', 'rssi', 'txpower', 'channel', 'channel_width', 'channel_band', 'security', 'phymode', 'noise_measurement', 'wifi_status')
        }),
        ('Date Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) 
        }),
    )