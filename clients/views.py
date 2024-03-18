from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Client
from .serializers import  ClientSerializer
from django.http import Http404
from rest_framework import permissions
from users.auth import TokenAuthentication
import requests

    

class ClientListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_interface_info(self, interface_name, client_ip, client_port):
        # Assuming the URL for querying interface info follows the format: http://clientIP:clientPort/device/wifi/interface/info?interfacename=interface
        url = f"http://{client_ip}:{client_port}/device/wifi/interface/info?interfacename={interface_name}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except:
            return None

    def update_interface_info(self, client_ip, client_port, interface_name):
        interface_info = self.get_interface_info(interface_name, client_ip, client_port)
        if interface_info:
            client = Client.objects.get(clientIP=client_ip, clientPort=client_port)
            for key, value in interface_info.items():
                setattr(client, key, value)
            setattr(client, 'status', True)
            client.save()
            return True
        else:
            setattr(client, 'status', False)
        return False
    def get(self, request):
        clients = Client.objects.filter(user=request.user)
        #update interface info
        for client in clients:
            self.update_interface_info(client.clientIP, client.clientPort, client.interface)

        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            client_ip = request.data.get('clientIP')
            client_port = request.data.get('clientPort')
            interface_name = request.data.get('interface')

            # Save initial data
            serializer.save()
            interface_info = self.get_interface_info(interface_name, client_ip, client_port)
            if interface_info:
                instance = serializer.instance
                for key, value in interface_info.items():
                    setattr(instance, key, value)
                setattr(instance, 'status', True)
                instance.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Initial data saved but failed to fetch the rest of the info"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientDetailAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        client = self.get_object(pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
