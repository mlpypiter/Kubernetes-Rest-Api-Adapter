from django.db import models
from common.models import BaseModel


class ServiceType(models.Model):
    class Meta:
        db_table = 'ServiceType'
    name = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.name


class Subscription(BaseModel):
    class Meta:
        db_table = 'subscription'
    customer = models.CharField(blank=False, max_length=255)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    term_subscription = models.BooleanField(blank=False, default=False)
    # service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    service_type = models.CharField(blank=False, max_length=255)
    subscription = models.CharField(blank=False, max_length=255)
    server_name_prefix = models.CharField(blank=False, max_length=255)
    package = models.IntegerField(blank=False, default=1)
    trunk_service_provider = models.IntegerField(blank=True, default=1)
    extra_call_record_package = models.IntegerField(null=True, default=1)
    demo = models.BooleanField(null=True, default=False)
    extra_duration_package =models.IntegerField(null=True, default=1)
    state = models.CharField(null=True, max_length=255, default="Not Initialized ")

    def __str__(self):
        return self.pk


class IpgServer(models.Model):
    class Meta:
        db_table = 'IpgServer'
    cpu = models.CharField(blank=False, max_length=255)
    ram = models.CharField(blank=False, max_length=255)
    disc = models.CharField(blank=False, max_length=255)
    widea_address = models.CharField(blank=False, max_length=255)
    local_ip = models.CharField(blank=False, max_length=255)
    external_ip = models.CharField(blank=False, max_length=255)
    external_ip = models.CharField(blank=False, max_length=255)
    server_name = models.CharField(blank=False, max_length=255)
    server_id = models.CharField(blank=False, max_length=255)
    state = models.IntegerField(blank=False, default=1)
    fqdn = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.pk


class WebcmServer(models.Model):
    class Meta:
        db_table = 'WebcmServer'
    address = models.CharField(blank=False, max_length=255)
    local_ip = models.CharField(blank=False, max_length=255)
    internal_ip = models.CharField(blank=False, max_length=255)
    server_name = models.CharField(blank=False, max_length=255)
    server_id = models.CharField(blank=False, max_length=255)
    state = models.IntegerField(blank=False, default=1)
    fqdn = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.pk


class Server(models.Model):
    class Meta:
        db_table = 'Server'
    action = models.CharField(blank=False, max_length=255, default="Stop")
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    status = models.CharField(blank=False, max_length=255, default="Active")

    def __str__(self):
        return self.pk
