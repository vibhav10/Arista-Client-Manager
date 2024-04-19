from rest_framework import serializers
from .models import  Client
from rest_framework.exceptions import ValidationError

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('ethernet_status', 'ssid_name', 'bssid', 'hwaddr', 'rssi', 'txpower', 
                            'channel', 'channel_width', 'channel_band', 'security', 'phymode', 
                            'noise_measurement', 'wifi_status', 'wifi_ip', 'operating_system', 
                            'transmit_rate', 'receive_rate', 'signal_quality', 'hostname', 
                            'ipv6_address', 'created_at', 'updated_at')
    


class ClientAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = 'user', 'ethernet_ip', 'interface_name', 'client_username', 'client_password', 'client_lab', 'description', 'client_port'

    def validate(self, data):
        try:
            instance = Client.objects.get(ethernet_ip=data.get('ethernet_ip'), client_port=data.get('client_port'))
            if instance:
                raise ValidationError("Client already added")
        except Client.DoesNotExist:
            pass
        return data
    

class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = 'ethernet_ip', 'interface_name', 'client_username', 'client_password', 'client_lab', 'description', 'client_port'
