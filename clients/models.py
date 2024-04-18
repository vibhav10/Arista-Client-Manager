from django.db import models
from users.models import User
# Create your models here.

class Client(models.Model):

    #stable fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ethernet_ip = models.GenericIPAddressField()
    client_port = models.IntegerField()
    client_username = models.CharField(max_length=255)
    client_password = models.CharField(max_length=255)
    client_lab = models.CharField(max_length=255)
    interface_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


    #dynamic fields
    ethernet_status = models.BooleanField(default=False)
    ssid_name = models.CharField(max_length=255, null=True, blank=True)
    bssid = models.CharField(max_length=255, null=True, blank=True)
    hwaddr = models.CharField(max_length=255, null=True, blank=True)
    rssi = models.IntegerField(null=True, blank=True)
    txpower = models.IntegerField(null=True, blank=True)
    channel = models.IntegerField(null=True, blank=True)
    channel_width = models.CharField(max_length=255, null=True, blank=True)
    channel_band = models.CharField(max_length=255, null=True, blank=True)
    security = models.CharField(max_length=255, null=True, blank=True)
    phymode = models.CharField(max_length=255, null=True, blank=True)
    noise_measurement = models.CharField(max_length=255, null=True, blank=True)
    wifi_status = models.CharField(max_length=255, default=False)
    wifi_ip = models.GenericIPAddressField(null=True, blank=True)
    operating_system = models.CharField(max_length=255, null=True, blank=True)
    transmit_rate = models.CharField(max_length=255, null=True, blank=True)
    receive_rate = models.CharField(max_length=255, null=True, blank=True)
    signal_quality = models.CharField(max_length=255, null=True, blank=True)
    hostname = models.CharField(max_length=255, null=True, blank=True)
    ipv6_address = models.TextField(null=True, blank=True)

    #date information
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)


    class Meta:
        #return error message ("message":"client aleready exists") if client with same ethernet_ip and client_port already exists
        unique_together = ('ethernet_ip', 'client_port')
        


    def __str__(self):
        return self.description + ' - ' + self.ethernet_ip + ':' + str(self.client_port)
    
    def save(self, *args, **kwargs):
        #if ethernet_status is false, clear all fields except stable fields
        if not self.ethernet_status:
            self.ssid_name = None
            self.bssid = None
            self.hwaddr = None
            self.rssi = None
            self.txpower = None
            self.channel = None
            self.channel_width = None
            self.channel_band = None
            self.security = None
            self.phymode = None
            self.noise_measurement = None
            self.wifi_status = False
        super(Client, self).save(*args, **kwargs)


