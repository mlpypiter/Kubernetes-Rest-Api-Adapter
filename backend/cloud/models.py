from django.db import models
from common.models import BaseModel


class ServiceType(BaseModel):
    class Meta:
        db_table = 'ServiceType'
    type = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.pk


class Subscription(BaseModel):
    class Meta:
        db_table = 'subscription'
    customer = models.CharField(blank=False, max_length=255)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    term_subscription = models.BooleanField(blank=False, default=False)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    subscription = models.CharField(blank=False, max_length=255)
    server_name_prefix = models.CharField(blank=False, max_length=255)
    package = models.IntegerField(blank=False, default=1)
    trunk_service_provider = models.IntegerField(blank=False, default=1)
    extra_call_record_package = models.IntegerField(blank=False, default=1)
    demo = models.BooleanField(blank=False, default=False)
    extra_duration_package =models.IntegerField(blank=False, default=1)
    servers = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.pk
