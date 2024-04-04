from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Client
from .serializers import  ClientSerializer
from django.http import Http404
from rest_framework import permissions
from users.auth import TokenAuthentication
import requests
from rest_framework import generics
import json

    

class ClientListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ClientSerializer

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)
    
    def get_interface_info(self, interface_name, client_ip, client_port):
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
            client = Client.objects.get(clientIP=client_ip, clientPort=client_port)
            setattr(client, 'status', False)
        return False
    
    
    def get(self, request):
        clients = self.get_queryset()
        if not clients:
            return Response({"message": "No clients found"}, status=status.HTTP_404_NOT_FOUND)
        for client in clients:
            self.update_interface_info(client.clientIP, client.clientPort, client.interface)
        serializer = self.serializer_class(clients, many=True)
        return Response(serializer.data)

    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            client_ip = request.data.get('clientIP')
            client_port = request.data.get('clientPort')
            interface_name = request.data.get('interface')
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



class ClientDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ClientSerializer

    def get_object(self, id):
        try:
            return Client.objects.get(id=id)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request):
        id = request.query_params.get('id')
        client = self.get_object(id)
        serializer = self.serializer_class(client)
        return Response(serializer.data)
    
    def put(self, request):
        client = self.get_object(id)
        serializer = self.serializer_class(client, data=request.data)
        if serializer.is_valid():
            client_ip = request.data.get('clientIP')
            client_port = request.data.get('clientPort')
            interface_name = request.data.get('interface')
            serializer.save()
            interface_info = ClientListAPIView.get_interface_info(self, interface_name, client_ip, client_port)
            if interface_info:
                for key, value in interface_info.items():
                    setattr(client, key, value)
                setattr(client, 'status', True)
                client.save()
                return Response(serializer.data)
            else:
                return Response({"message": "Data updated but failed to fetch the rest of the info"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        id_list_str = request.data.get('id')
        id_list = json.loads(id_list_str)
        print(id_list)
        for id in id_list:
            client = self.get_object(id)
            client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
