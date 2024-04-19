from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import permissions
from users.auth import TokenAuthentication
import requests
from rest_framework import generics
import json
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from clients.models import Client
from datetime import datetime


'''
This class is used to retrieve all clients and add a new client.
'''
class ClientSpeedTestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    
    def get_speed_test_results(self,ethernet_ip, client_port):
        url = f"http://{ethernet_ip}:{client_port}/device/traffic/speedtest/results"
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                return response.json()
        except:
            return None

    def convert_data(self, speed_test_results):
        transformed_data = {}
        downloadspeed = {}
        uploadspeed = {}
        download = {}
        upload = {}
        idlelatency = {}
        downloadlatency = {}
        uploadlatency = {}
        for result in speed_test_results:
            timestamp = datetime.fromtimestamp(result['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            uploadspeed[timestamp] = result['uploadspeed']
            downloadspeed[timestamp] = result['downloadspeed']
            download[timestamp] = result['download']
            upload[timestamp] = result['upload']
            idlelatency[timestamp] = result['idlelatency']
            downloadlatency[timestamp] = result['downloadlatency']
            uploadlatency[timestamp] = result['uploadlatency']
        
        transformed_data['download_speed'] = downloadspeed
        transformed_data['upload_speed'] = uploadspeed
        transformed_data['download'] = download
        transformed_data['upload'] = upload
        transformed_data['idle_latency'] = idlelatency
        transformed_data['download_latency'] = downloadlatency
        transformed_data['upload_latency'] = uploadlatency
        return transformed_data
    '''
    API methods
    '''

    def get(self, request):
        user = request.user
        client_id = request.data.get('id')
        if client_id is None:
            return Response({'error': 'Client ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            client = Client.objects.get(id=client_id, user=user)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        speed_test_results = self.get_speed_test_results(client.ethernet_ip, client.client_port)
        if speed_test_results is None:
            return Response({'error': 'Failed to retrieve speed test results'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print(speed_test_results)
        converted_data = self.convert_data(speed_test_results)
        return Response(converted_data, status=status.HTTP_200_OK)

