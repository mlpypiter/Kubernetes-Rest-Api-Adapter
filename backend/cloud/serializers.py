from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from common.exception import CustomException
from .models import Subscription, ServiceType, Server


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(required=False)
    start_date = serializers.CharField(required=False)
    end_date = serializers.CharField(required=False)
    term_subscription = serializers.BooleanField(required=False)
    service_type = serializers.IntegerField(required=False)
    subscription = serializers.CharField(required=False)
    server_name_prefix = serializers.CharField(required=False)
    package = serializers.IntegerField(required=False)
    trunk_service_provider = serializers.IntegerField(required=False)
    extra_call_record_package = serializers.IntegerField(required=False)
    demo = serializers.BooleanField(required=False)
    extra_duration_package = serializers.IntegerField(required=False)

    default_error_messages = {
        'invalid_customer': _('customer is invalid.'),
        'invalid_start_date': _('start_date is not selected.'),
        'invalid_end_date': _('end_date is invalid.'),
        'invalid_term': _('term is selected.'),
        'invalid_type': _('type is invalid.'),
        'invalid_subscription': _('subscription was not selected.'),
        'invalid_name': _('name was not selected.'),
        'invalid_package': _('package was not selected.'),
        'invalid_trunk': _('trunk was not selected.'),
        'invalid_call_record': _('call_record was not selected.'),
        'invalid_demo': _('demo was not selected.'),
        'invalid_duration_package': _('duration_package was not selected.'),
    }

    class Meta:
        model = Subscription
        fields = ("customer", "start_date", "end_date", "term_subscription", "service_type", "subscription",
                  "server_name_prefix", "package", "trunk_service_provider", "extra_call_record_package", "demo",
                  "extra_duration_package")

    def validate(self, attrs):
        customer = attrs.get("customer")
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        term_subscription = attrs.get("term_subscription")
        service_type = attrs.get("service_type")
        subscription = attrs.get("subscription")
        server_name_prefix = attrs.get("server_name_prefix")
        package = attrs.get("package")
        trunk_service_provider = attrs.get("trunk_service_provider")
        extra_call_record_package = attrs.get("extra_call_record_package")
        demo = attrs.get("demo")
        extra_duration_package = attrs.get("extra_duration_package")

        if not customer:
            raise CustomException(code=10, message=self.error_messages['invalid_customer'])
        if not start_date:
            raise CustomException(code=11, message=self.error_messages['invalid_start_date'])
        if not end_date:
            raise CustomException(code=12, message=self.error_messages['invalid_end_date'])
        if not term_subscription:
            raise CustomException(code=13, message=self.error_messages['invalid_term'])
        if not service_type:
            raise CustomException(code=14, message=self.error_messages['invalid_type'])
        if not subscription:
            raise CustomException(code=15, message=self.error_messages['invalid_subscription'])
        if not server_name_prefix:
            raise CustomException(code=16, message=self.error_messages['invalid_name'])
        if not package:
            raise CustomException(code=17, message=self.error_messages['invalid_package'])
        if not trunk_service_provider:
            raise CustomException(code=18, message=self.error_messages['invalid_trunk'])
        if not extra_call_record_package:
            raise CustomException(code=19, message=self.error_messages['invalid_call_record'])
        if not demo:
            raise CustomException(code=20, message=self.error_messages['invalid_demo'])
        if not extra_duration_package:
            raise CustomException(code=21, message=self.error_messages['invalid_duration_package'])

        try:
            serviceType = ServiceType.objects.get(id=service_type)
            attrs['serviceType'] = serviceType
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=14, message=self.error_messages['invalid_type'])


class ServerStatusSerializer(serializers.ModelSerializer):
    server_ids = serializers.IntegerField(required=False)
    action = serializers.CharField(required=False)
    server_type = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_serverid': _('serverid is invalid.'),
        'invalid_action': _('action is not invalid.'),
        'invalid_server_type': _('server_type is invalid.'),
    }

    class Meta:
        model = Subscription
        fields = ("server_ids", "action", "server_type")

    def validate(self, attrs):
        server_ids = attrs.get("server_ids")
        action = attrs.get("action")
        server_type = attrs.get("server_type")

        if not server_ids:
            raise CustomException(code=10, message=self.error_messages['invalid_serverid'])
        if not action:
            raise CustomException(code=11, message=self.error_messages['invalid_action'])
        if not server_type:
            raise CustomException(code=12, message=self.error_messages['invalid_server_type'])

        try:
            server = Server.objects.get(id=server_ids)
            attrs['server'] = server
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=14, message=self.error_messages['invalid_serverid'])


class ChangeServerSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(required=False)
    server_id = serializers.CharField(required=False)
    server_type = serializers.CharField(required=False)

    default_error_messages = {
        'invalid_status': _('status is invalid.'),
        'invalid_server_id': _('server_id is not invalid.'),
        'invalid_server_type': _('server_type is invalid.'),
    }

    class Meta:
        model = Subscription
        fields = ("status", "server_id", "server_type")

    def validate(self, attrs):
        status = attrs.get("status")
        server_id = attrs.get("server_id")
        server_type = attrs.get("server_type")

        if not status:
            raise CustomException(code=10, message=self.error_messages['invalid_status'])
        if not server_id:
            raise CustomException(code=11, message=self.error_messages['invalid_server_id'])
        if not server_type:
            raise CustomException(code=12, message=self.error_messages['invalid_server_type'])

        try:
            server = Server.objects.get(id=server_id)
            attrs['server'] = server
            return attrs
        except ObjectDoesNotExist:
            raise CustomException(code=14, message=self.error_messages['invalid_server_id'])
