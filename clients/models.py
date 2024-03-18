from django.db import models
from users.models import User
# Create your models here.

# class Group(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name
    

class Client(models.Model):
    # group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clientName = models.CharField(max_length=255)
    clientIP = models.GenericIPAddressField()
    clientPort = models.IntegerField()
    clientUsername = models.CharField(max_length=255)
    clientPassword = models.CharField(max_length=255)
    clientLab = models.CharField(max_length=255)
    traffic_profile = models.CharField(max_length=255)
    description = models.TextField()
    ssid = models.CharField(max_length=255, null=True, blank=True)
    bssid = models.CharField(max_length=255, null=True, blank=True)
    hwaddr = models.CharField(max_length=255, null=True, blank=True)
    rssi = models.IntegerField(null=True, blank=True)
    txpower = models.IntegerField(null=True, blank=True)
    channel = models.IntegerField(null=True, blank=True)
    channel_width = models.CharField(max_length=255, null=True, blank=True)
    channel_band = models.CharField(max_length=255, null=True, blank=True)
    security = models.CharField(max_length=255, null=True, blank=True)
    phymode = models.CharField(max_length=255, null=True, blank=True)
    phyrate = models.CharField(max_length=255, null=True, blank=True)
    noise_measurement = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
