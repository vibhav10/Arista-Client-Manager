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
    interface = models.CharField(max_length=255)
    description = models.TextField()

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
    phyrate = models.CharField(max_length=255, null=True, blank=True)
    noise_measurement = models.CharField(max_length=255, null=True, blank=True)
    wifi_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        unique_together = ('ethernet_ip', 'client_port')

    def __str__(self):
        return self.description + ' - ' + self.clientIP + ':' + str(self.clientPort)
    
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
            self.phyrate = None
            self.noise_measurement = None
            self.wifi_status = False
        super(Client, self).save(*args, **kwargs)


