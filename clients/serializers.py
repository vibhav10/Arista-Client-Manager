from rest_framework import serializers
from .models import  Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = 'ethernet_ip', 'interface_name', 'client_username', 'client_password', 'client_lab', 'description', 'client_port'