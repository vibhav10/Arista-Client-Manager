from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Client
from .serializers import  ClientSerializer, ClientAddSerializer, ClientUpdateSerializer
from django.http import Http404
from rest_framework import permissions
from users.auth import TokenAuthentication
import requests
from rest_framework import generics
import json
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
    


'''
This class is used to retrieve all clients and add a new client.
'''
class ClientListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ClientSerializer

    '''
    This dictionary contains the mappings between the Wifi-Agent API fields and the model fields.
    '''

    API_TO_CLIENT_MODEL_MAPPING = {
    "ssidname": "ssid_name",
    "bssid": "bssid",
    "hwaddr": "hwaddr",
    "rssi": "rssi",
    "txpower": "txpower",
    "channel": "channel",
    "channelwidth": "channel_width",
    "channelband": "channel_band",
    "security": "security",
    "phymode": "phymode",
    "noisemeasurement": "noise_measurement",
    "transmitrate": "transmit_rate",
    "receiverate": "receive_rate",
    "signalquality": "signal_quality",
    "status": "wifi_status",
    "os": "operating_system",
    "ipv4address": "wifi_ip",
    "hostname": "hostname",
    "ipv6addresses": "ipv6_address"
    }

    '''
    Helper methods
    '''

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)
    
    def check_reachability(self, ethernet_ip, client_port):
        url = f"http://{ethernet_ip}:{client_port}/version"
        print(url)
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                return True
        except:
            return False
    
    def get_interface_info(self, interface_name, ethernet_ip, client_port):
        url = f"http://{ethernet_ip}:{client_port}/device/wifi/interface/info?interfacename={interface_name}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                return response.json()
        except:
            return None

    def update_interface_info(self, ethernet_ip, client_port, interface_name):
        try:
            interface_info = self.get_interface_info(interface_name, ethernet_ip, client_port)
            if interface_info:
                client = Client.objects.get(ethernet_ip=ethernet_ip, client_port=client_port)
                for api_key, model_field in self.API_TO_CLIENT_MODEL_MAPPING.items():
                    if api_key in interface_info:
                        setattr(client, model_field, interface_info[api_key])
                setattr(client, 'ethernet_status', True)
                client.save()
            else:
                client = Client.objects.get(ethernet_ip=ethernet_ip, client_port=client_port)
                setattr(client, 'ethernet_status', False)
                client.save()
        except:
            pass
        
    
    '''
    API methods
    '''
    
    @swagger_auto_schema(
        responses={200: ClientSerializer(many=True)},
        operation_summary="Retrieve all clients",
    )
    def get(self, request):
        clients = self.get_queryset()
        if not clients:
            return Response({"message": "No clients found"}, status=status.HTTP_404_NOT_FOUND)
        for client in clients:
            self.update_interface_info(client.ethernet_ip, client.client_port, client.interface_name)
        clients = self.get_queryset().order_by('-created_at')
        serializer = self.serializer_class(clients, many=True)
        return Response(serializer.data)

    

    @swagger_auto_schema(
        request_body=ClientSerializer,
        responses={201: 'Client added successfully.', 400: 'Client could not be reached'},
        operation_summary="Add a client",
    )
    def post(self, request):
        user = self.request.user
        request.data['user'] = user.id
        print(request.data)
        serializer = ClientAddSerializer(data=request.data)
        if serializer.is_valid():
            ethernet_ip = request.data.get('ethernet_ip')
            client_port = request.data.get('client_port')
            if not self.check_reachability(ethernet_ip, client_port): # Check if client is reachable
                return Response({"message": "Client could not be reached"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"message": "Client added successfully."}, status=status.HTTP_201_CREATED) 
        elif 'Client already added' in str(serializer.errors):
                return Response({"message": "Client already added"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


'''
This class is used to retrieve, update and delete a client.
'''
class ClientModifyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ClientSerializer


    '''
    Helper methods
    '''

    # Get the client object
    def get_object(self, id):
        try:
            return Client.objects.get(user=self.request.user, id=id)
        except Client.DoesNotExist:
            raise Http404


    
    '''
    API methods
    '''

    
    @swagger_auto_schema( 
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={200: ClientSerializer},
        operation_summary="Retrieve a client",
    )
    # Retrieve a client
    def get(self, request):
        id = request.query_params.get('id')
        client = self.get_object(id)
        serializer = self.serializer_class(client)
        return Response(serializer.data)
    

    @swagger_auto_schema(
        request_body=ClientUpdateSerializer,
        responses={201: 'Client updated successfully.', 400: 'Client could not be reached'},
        operation_summary="Update a client",
    )
    # Update a client
    def put(self, request):
        id = request.data.get('id')
        client = self.get_object(id)
        serializer = ClientUpdateSerializer(client, data=request.data)
        
        if serializer.is_valid():
            ethernet_ip = request.data.get('ethernet_ip')
            client_port = request.data.get('client_port')
            if not ClientListCreateAPIView().check_reachability(ethernet_ip, client_port):
                return Response({"message": "Update cannot proceed as the client is not accessible."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"message": "Client updated successfully."}, status=status.HTTP_201_CREATED) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            },
            required=['id'],
        ),
        responses={204: 'Client deleted successfully.', 400: 'Client could not be deleted'},
        operation_summary="Delete a client",
    )
    # Delete a client
    def delete(self, request):
        id_list_str = request.data.get('id')
        id_list = json.loads(id_list_str)
        print(id_list)
        try:
            for id in id_list:
                client = self.get_object(id)
                client.delete()
            return Response({"message": "Client deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"message": "Client could not be deleted"}, status=status.HTTP_400_BAD_REQUEST)
